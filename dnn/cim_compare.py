#!/usr/bin/env python3
"""
R4 revision: compare several binary networks (and decoders) under the same CIM error cases.

Networks (all binary weights +-1, binary 0/1 activations, trained from scratch with STE):
  mlp        : FC 784-256 -> FC 256-10
  cnn_small  : conv3x3 16 -> pool -> conv3x3 32 -> pool -> FC 800-10     (the network in the paper)
  cnn_wide   : conv3x3 32 -> pool -> conv3x3 64 -> pool -> FC 1600-10
Datasets: mnist, fashion (Fashion-MNIST), both binarized at 0.5.

Error cases (each column readout decoded as clip(round(k + e), 0, 8), W+/W- column pairs):
  ideal
  PVT, supply-tracking decoder : measured per-count error of each of the 45 conditions (pvt_results.csv)
  PVT, fixed-threshold decoder : same data decoded with absolute nominal thresholds
  worst array corner + 3 sigma : measured array table (array_pvt_out/per_run.csv) + sigma 0.036
  random sigma 0.2 / 0.3

Usage (venv active, in the folder with pvt_results.csv and array_pvt_out/):
  python3 cim_compare.py train            # trains 6 models (3 nets x 2 datasets), saves cmp_out/*.pt
  python3 cim_compare.py eval pvt_results.csv array_pvt_out/per_run.csv
  add --fake to test without downloading data
Runtime on a laptop CPU: training roughly 1-2 h (cnn_wide dominates), eval roughly 30-60 min.
PVT cases are exact but cached: a table whose rounded counts equal the true counts gives exactly the
ideal accuracy, so only distinct decoded-count maps are simulated.
Outputs: cmp_out/compare.csv, cmp_out/compare_pvt_detail.csv, cmp_out/fig_compare.png
"""
import sys, os, csv
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

torch.manual_seed(0); np.random.seed(0)
OUT = "cmp_out"; os.makedirs(OUT, exist_ok=True)
FAKE = "--fake" in sys.argv
args = [a for a in sys.argv[1:] if a != "--fake"]
NETS = ["mlp", "cnn_small", "cnn_wide"]
DATA = ["mnist", "fashion"]
EPOCHS = {"mlp": 10, "cnn_small": 6, "cnn_wide": 5}

# ------------------------------------------------------------------ data
_cache = {}
def load(name):
    if name in _cache: return _cache[name]
    if FAKE:
        x = (torch.rand(1200, 1, 28, 28) > 0.5).float(); y = torch.randint(0, 10, (1200,))
        _cache[name] = (x[:1000], y[:1000], x[1000:], y[1000:]); return _cache[name]
    from torchvision import datasets
    D = datasets.MNIST if name == "mnist" else datasets.FashionMNIST
    tr, te = D("data", train=True, download=True), D("data", train=False, download=True)
    f = lambda d: (d.data.float().div(255).unsqueeze(1) > 0.5).float()
    _cache[name] = (f(tr), tr.targets, f(te), te.targets); return _cache[name]

# ------------------------------------------------------------------ model
class SignSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x): return torch.where(x > 0, torch.ones_like(x), -torch.ones_like(x))
    @staticmethod
    def backward(ctx, g): return g

class StepSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x); return (x > 0).float()
    @staticmethod
    def backward(ctx, g):
        (x,) = ctx.saved_tensors; return g * (x.abs() < 1).float()

SPECS = {   # (kind, size); conv layers are followed by 2x2 max-pool
    "mlp":       [("fc", 784, 256), ("fc", 256, 10)],
    "cnn_small": [("conv", 1, 16), ("conv", 16, 32), ("fc", 800, 10)],
    "cnn_wide":  [("conv", 1, 32), ("conv", 32, 64), ("fc", 1600, 10)],
}

class BNet(nn.Module):
    def __init__(s, kind):
        super().__init__(); s.spec = SPECS[kind]
        s.W = nn.ParameterList(); s.BN = nn.ModuleList()
        for t, a, b in s.spec:
            s.W.append(nn.Parameter(torch.randn(b, a, 3, 3) * .1 if t == "conv" else torch.randn(b, a) * .1))
            s.BN.append(nn.BatchNorm2d(b) if t == "conv" else nn.BatchNorm1d(b))

    def layers(s, x, conv, fc, wfun):
        last = len(s.spec) - 1
        for i, (t, _, _) in enumerate(s.spec):
            w = wfun(s.W[i])
            if t == "conv":
                x = s.BN[i](conv(x, w)); x = F.max_pool2d(StepSTE.apply(x) if s.training else (x > 0).float(), 2)
            else:
                x = s.BN[i](fc(x.flatten(1), w))
                if i < last: x = StepSTE.apply(x) if s.training else (x > 0).float()
        return x

    def forward(s, x):
        return s.layers(x, F.conv2d, F.linear, SignSTE.apply)

# ------------------------------------------------------------------ CIM inference
class Err:
    def __init__(s, bias=0., sigma=0., etab=None, neg=None):
        s.bias, s.sigma, s.neg = bias, sigma, neg
        s.etab = None if etab is None else torch.tensor(np.asarray(etab), dtype=torch.float32)

def readout(k, E):
    e = E.bias + (E.etab[k.long()] if E.etab is not None else 0)
    if E.sigma > 0: e = e + E.sigma * torch.randn_like(k)
    return (k + e).round().clamp(0, 8)

def cim_mac(xp, w, E):
    B, L, n = xp.shape; pad = (-n) % 8
    if pad: xp = F.pad(xp, (0, pad)); w = F.pad(w, (0, pad))
    C = xp.shape[-1] // 8; xc = xp.view(B, L, C, 8)
    kp = torch.einsum("blcr,ocr->blco", xc, (w > 0).float().view(-1, C, 8))
    kn = torch.einsum("blcr,ocr->blco", xc, (w < 0).float().view(-1, C, 8))
    return (readout(kp, E) - readout(kn, E.neg or E)).sum(2)

def make_ops(E):
    def conv(x, w4):
        B, _, H, W = x.shape; o = w4.shape[0]
        y = cim_mac(F.unfold(x, 3).transpose(1, 2), w4.flatten(1), E)
        return y.transpose(1, 2).reshape(B, o, H - 2, W - 2)
    def fc(x, w): return cim_mac(x.unsqueeze(1), w, E).squeeze(1)
    return conv, fc

@torch.no_grad()
def acc(net, x, y, E, bs=100):
    net.eval(); conv, fc = make_ops(E); hit = 0
    for i in range(0, len(x), bs):
        out = net.layers(x[i:i+bs], conv, fc, lambda p: torch.where(p > 0, 1., -1.))
        hit += (out.argmax(1) == y[i:i+bs]).sum().item()
    return 100 * hit / len(x)

# ------------------------------------------------------------------ commands
def train():
    for d in DATA:
        xtr, ytr, xte, yte = load(d)
        for k in NETS:
            torch.manual_seed(0); net = BNet(k); opt = torch.optim.Adam(net.parameters(), 3e-3)
            for e in range(1 if FAKE else EPOCHS[k]):
                net.train(); perm = torch.randperm(len(xtr))
                for i in range(0, len(xtr), 128):
                    idx = perm[i:i+128]; loss = F.cross_entropy(net(xtr[idx]), ytr[idx])
                    opt.zero_grad(); loss.backward(); opt.step()
                    with torch.no_grad():
                        for p in net.W: p.clamp_(-1, 1)
                net.eval()
                with torch.no_grad(): a = (net(xte).argmax(1) == yte).float().mean().item() * 100
                print(f"{d:8s} {k:10s} epoch {e+1}: {a:.2f}%", flush=True)
            torch.save(net.state_dict(), f"{OUT}/{d}_{k}.pt")

def pvt_tables(path):
    import pandas as pd
    df = pd.read_csv(path, sep=r"\s+", header=None, names=["corner", "vdd", "temp", "k", "v"])
    nom = df[(df.corner == "tt") & (df.vdd == 1.8) & (df.temp == 27)].sort_values("k")
    vn = nom.v.values; kk = np.arange(9.0)
    T = []
    for (c, v, t), g in df.groupby(["corner", "vdd", "temp"]):
        g = g.sort_values("k")
        track = np.interp(-(g.v.values / v), -(vn / 1.8), kk) - kk     # supply-tracking (V/VDD)
        fixed = np.interp(-g.v.values, -vn, kk) - kk                    # fixed absolute thresholds
        T.append((c, v, t, track, fixed))
    return T

def array_table(path):
    import pandas as pd
    R = pd.read_csv(path)
    wc = R.groupby(["corner", "vdd", "temp"]).err_corr.apply(lambda s: s.abs().max()).idxmax()
    g = R[(R.corner == wc[0]) & (R.vdd == wc[1]) & (R.temp == wc[2])]
    km = g.groupby("k").err_corr.agg(lambda s: s.loc[s.abs().idxmax()])
    return np.interp(np.arange(9), km.index.values, km.values)

def evaluate(pvt_path, arr_path):
    T = pvt_tables(pvt_path); at = array_table(arr_path)
    rows = [("dataset", "network", "ideal", "pvt_track_min", "pvt_track_mean", "pvt_fixed_min", "pvt_fixed_mean",
             "worst_array_3sigma", "sigma_0.2", "sigma_0.3")]
    detail = [("dataset", "network", "corner", "vdd", "temp", "acc_track", "acc_fixed")]
    for d in DATA:
        _, _, x, y = load(d)
        for k in NETS:
            net = BNet(k); net.load_state_dict(torch.load(f"{OUT}/{d}_{k}.pt")); net.eval()
            ideal = acc(net, x, y, Err())
            at_, af_ = [], []
            cache = {}
            def det(tab):   # deterministic table: accuracy depends only on the decoded count per k -> cache
                key = tuple(np.clip(np.round(np.arange(9) + tab), 0, 8).astype(int))
                if key not in cache:
                    cache[key] = ideal if key == tuple(range(9)) else acc(net, x, y, Err(etab=tab))
                return cache[key]
            for c, v, t, tr, fx in T:
                a1 = det(tr); a2 = det(fx)
                at_.append(a1); af_.append(a2); detail.append((d, k, c, v, t, round(a1, 2), round(a2, 2)))
            wa = acc(net, x, y, Err(etab=at, sigma=.036))
            s2 = acc(net, x, y, Err(sigma=.2)); s3 = acc(net, x, y, Err(sigma=.3))
            r = (d, k, ideal, min(at_), np.mean(at_), min(af_), np.mean(af_), wa, s2, s3)
            rows.append(tuple(r[:2]) + tuple(round(float(q), 2) for q in r[2:]))
            print(f"   ({len(cache)} distinct decoded-count maps simulated for the 90 PVT cases)")
            print(f"{d:8s} {k:10s} ideal {ideal:6.2f} | PVT track min {min(at_):6.2f} | PVT fixed min {min(af_):6.2f} "
                  f"mean {np.mean(af_):6.2f} | worst array+3s {wa:6.2f} | s0.2 {s2:6.2f} s0.3 {s3:6.2f}", flush=True)
    csv.writer(open(f"{OUT}/compare.csv", "w")).writerows(rows)
    csv.writer(open(f"{OUT}/compare_pvt_detail.csv", "w")).writerows(detail)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
        labels = ["ideal", "PVT\ntracking\n(min)", "PVT\nfixed thr.\n(min)", "worst array\n+3σ", "σ=0.2", "σ=0.3"]
        idx = [2, 3, 5, 7, 8, 9]
        for a, d in zip(ax, DATA):
            rr = [r for r in rows[1:] if r[0] == d]
            for j, r in enumerate(rr):
                a.bar(np.arange(6) + (j - 1) * 0.27, [r[i] for i in idx], 0.27, label=r[1])
            a.set_xticks(range(6)); a.set_xticklabels(labels, fontsize=7); a.set_title(d); a.grid(axis="y", alpha=.3)
        ax[0].set_ylabel("test accuracy (%)"); ax[0].legend(fontsize=7)
        plt.tight_layout(); plt.savefig(f"{OUT}/fig_compare.png", dpi=200); print("wrote", f"{OUT}/fig_compare.png")
    except Exception as ex:
        print("plot skipped:", ex)
    print("wrote", f"{OUT}/compare.csv")

if __name__ == "__main__":
    cmd = args[0] if args else "train"
    if cmd == "train": train()
    elif cmd == "eval": evaluate(args[1], args[2])
    else: sys.exit(__doc__)
