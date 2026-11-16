#!/usr/bin/env python3
"""
CIM noise injection on a binary CNN (MNIST).

Mapping (what the array physically does):
  - inputs are 0/1 (RWL pulse or not), weights are +-1 stored as a column PAIR:
    W+ = (w>0), W- = (w<=0), each cell computes AND(input, weight bit)
  - a MAC of length n is split into chunks of 8 rows (one column = 8 cells)
  - each column readout is a count k in 0..8, decoded as round(k + e), clipped to 0..8
  - result = sum over chunks (k_pos - k_neg), then digital BN + threshold

Error e on each column readout (counts):
  e = bias + e_table[k] - dz * n_zero_rows + sigma * N(0,1)
    bias   : constant systematic error (e.g. PVT drift)
    e_table: optional per-count systematic error from pvt_results.csv
    dz     : input-dependent offset per inactive row (counts); readout is LOWER when
             rows are inactive (higher column V = fewer counts)
    sigma  : random error (mismatch, noise)

Usage:
  python3 cim_dnn.py train                     # train + save model.pt (~ few min on CPU)
  python3 cim_dnn.py sweep                     # accuracy vs bias / sigma / dz
  python3 cim_dnn.py scenarios                 # named scenarios from the findings doc
  python3 cim_dnn.py table pvt_results.csv     # per-corner accuracy using real column data
  python3 cim_dnn.py pairs [array_pvt_out/per_run.csv]   # unmatched W+/W- column errors (R1)
  add --fake to any command to test the pipeline on random data (no MNIST needed)
"""
import sys, os, csv, math
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

torch.manual_seed(0); np.random.seed(0)
OUT = "dnn_out"; os.makedirs(OUT, exist_ok=True)
FAKE = "--fake" in sys.argv
args = [a for a in sys.argv[1:] if a != "--fake"]
dev = "cpu"


# ---------------------------------------------------------------- data
def load_mnist():
    if FAKE:
        n = 2000
        x = (torch.rand(n, 1, 28, 28) > 0.5).float()
        y = torch.randint(0, 10, (n,))
        return x, y, x[:500], y[:500]
    from torchvision import datasets
    tr = datasets.MNIST("data", train=True, download=True)
    te = datasets.MNIST("data", train=False, download=True)
    f = lambda d: (d.data.float().div(255).unsqueeze(1) > 0.5).float()
    return f(tr), tr.targets, f(te), te.targets


# ---------------------------------------------------------------- model
class SignSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        return torch.where(x > 0, torch.ones_like(x), -torch.ones_like(x))
    @staticmethod
    def backward(ctx, g):
        return g

class StepSTE(torch.autograd.Function):          # output 0/1
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return (x > 0).float()
    @staticmethod
    def backward(ctx, g):
        (x,) = ctx.saved_tensors
        return g * (x.abs() < 1).float()

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Parameter(torch.randn(16, 1, 3, 3) * 0.1)
        self.c2 = nn.Parameter(torch.randn(32, 16, 3, 3) * 0.1)
        self.fc = nn.Parameter(torch.randn(10, 800) * 0.1)
        self.b1 = nn.BatchNorm2d(16)
        self.b2 = nn.BatchNorm2d(32)
        self.b3 = nn.BatchNorm1d(10)

    def forward(self, x):                         # ideal / training path
        w1, w2, w3 = SignSTE.apply(self.c1), SignSTE.apply(self.c2), SignSTE.apply(self.fc)
        x = StepSTE.apply(self.b1(F.conv2d(x, w1)));  x = F.max_pool2d(x, 2)
        x = StepSTE.apply(self.b2(F.conv2d(x, w2)));  x = F.max_pool2d(x, 2)
        return self.b3(F.linear(x.flatten(1), w3))


# ---------------------------------------------------------------- CIM inference
class Err:
    def __init__(s, bias=0., sigma=0., dz=0., etab=None, rnd=True, neg=None):
        s.bias, s.sigma, s.dz, s.rnd = bias, sigma, dz, rnd
        s.etab = None if etab is None else torch.tensor(etab, dtype=torch.float32)
        s.neg = neg      # optional separate Err for the W- column (unmatched pair); None = same as W+

def readout(k, nz, E):
    e = E.bias - E.dz * nz
    if E.etab is not None:
        e = e + E.etab[k.long()]
    if E.sigma > 0:
        e = e + E.sigma * torch.randn_like(k)
    v = k + e
    return v.round().clamp(0, 8) if E.rnd else v.clamp(0, 8)

def cim_mac(xp, w, E):
    """xp: (B,L,n) 0/1 inputs, w: (out,n) +-1 weights -> (B,L,out) signed sums via 8-row columns."""
    B, L, n = xp.shape
    pad = (-n) % 8
    if pad:
        xp = F.pad(xp, (0, pad)); w = F.pad(w, (0, pad), value=0.)   # pad rows: input 0, weight bit 0
    C = xp.shape[-1] // 8
    xc = xp.view(B, L, C, 8)
    wp = (w > 0).float().view(-1, C, 8)                               # W+ bits
    wn = (w < 0).float().view(-1, C, 8)                               # W- bits (padding stays 0)
    kp = torch.einsum("blcr,ocr->blco", xc, wp)
    kn = torch.einsum("blcr,ocr->blco", xc, wn)
    nz = (8 - xc.sum(-1, keepdim=True))                               # inactive rows per chunk
    dp, dn = readout(kp, nz, E), readout(kn, nz, E.neg if E.neg is not None else E)
    return (dp - dn).sum(2)

def conv_cim(x, w4, E):
    B, Cin, H, W = x.shape
    out, _, kh, kw = w4.shape
    u = F.unfold(x, (kh, kw)).transpose(1, 2)                         # (B,L,n)
    y = cim_mac(u, w4.flatten(1), E)                                  # (B,L,out)
    Ho, Wo = H - kh + 1, W - kw + 1
    return y.transpose(1, 2).reshape(B, out, Ho, Wo)

@torch.no_grad()
def infer(net, x, E, bs=200):
    net.eval()
    w1, w2, w3 = [torch.where(p > 0, 1., -1.) for p in (net.c1, net.c2, net.fc)]
    outs = []
    for i in range(0, len(x), bs):
        a = x[i:i + bs]
        a = (net.b1(conv_cim(a, w1, E)) > 0).float(); a = F.max_pool2d(a, 2)
        a = (net.b2(conv_cim(a, w2, E)) > 0).float(); a = F.max_pool2d(a, 2)
        y = cim_mac(a.flatten(1).unsqueeze(1), w3, E).squeeze(1)
        outs.append(net.b3(y))
    return torch.cat(outs)

def acc(net, x, y, E):
    return (infer(net, x, E).argmax(1) == y).float().mean().item() * 100


# ---------------------------------------------------------------- commands
def train():
    xtr, ytr, xte, yte = load_mnist()
    net = Net(); opt = torch.optim.Adam(net.parameters(), 3e-3)
    ep = 1 if FAKE else 6
    for e in range(ep):
        net.train(); perm = torch.randperm(len(xtr))
        for i in range(0, len(xtr), 128):
            idx = perm[i:i + 128]
            loss = F.cross_entropy(net(xtr[idx]), ytr[idx])
            opt.zero_grad(); loss.backward(); opt.step()
            with torch.no_grad():
                for p in (net.c1, net.c2, net.fc): p.clamp_(-1, 1)
        net.eval()
        with torch.no_grad():
            a = (net(xte).argmax(1) == yte).float().mean().item() * 100
        print(f"epoch {e+1}/{ep}  float-BNN test acc {a:.2f}%", flush=True)
    torch.save(net.state_dict(), f"{OUT}/model.pt")
    print("saved", f"{OUT}/model.pt")

def get():
    net = Net(); net.load_state_dict(torch.load(f"{OUT}/model.pt")); net.eval()
    _, _, xte, yte = load_mnist()
    return net, xte, yte

def sweep():
    net, x, y = get()
    base = acc(net, x, y, Err())
    print(f"ideal CIM (no error): {base:.2f}%")
    rows = [("param", "value", "acc_round", "acc_noround")]
    grids = {"bias": [-1, -.8, -.6, -.5, -.4, -.2, 0, .2, .4, .5, .6, .8, 1],
             "sigma": [0, .1, .2, .3, .4, .5, .7, 1.0],
             "dz": [0, .01, .02, .04, .064, .1, .15, .2]}
    for p, g in grids.items():
        for v in g:
            a1 = acc(net, x, y, Err(**{p: v}))
            a2 = acc(net, x, y, Err(**{p: v}, rnd=False))
            rows.append((p, v, round(a1, 2), round(a2, 2)))
            print(f"{p:6s} {v:6.3f}  rounded {a1:6.2f}%   unrounded {a2:6.2f}%", flush=True)
    csv.writer(open(f"{OUT}/sweep.csv", "w")).writerows(rows)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
        for a, p in zip(ax, grids):
            r = [t for t in rows[1:] if t[0] == p]
            a.plot([t[1] for t in r], [t[2] for t in r], "o-", label="decoded (rounded)")
            a.plot([t[1] for t in r], [t[3] for t in r], "s--", label="unrounded")
            a.set_xlabel(f"{p} (counts)" if p != "dz" else "dz (counts per inactive row)")
            a.set_ylabel("test acc (%)"); a.grid(alpha=.3)
        ax[0].legend(); plt.tight_layout(); plt.savefig(f"{OUT}/fig_dnn_sweep.png", dpi=150)
        print("wrote", f"{OUT}/fig_dnn_sweep.png")
    except Exception as ex:
        print("plot skipped:", ex)

def scenarios():
    net, x, y = get()
    S = [
        ("ideal", Err()),
        ("ours: PVT 0.29 + corrected offset (0.095/8 per row) + sigma 0.012", Err(bias=.29, dz=.095/8, sigma=.012)),
        ("ours, opposite PVT sign", Err(bias=-.29, dz=.095/8, sigma=.012)),
        ("no offset correction (0.51/8 per row) + PVT 0.29", Err(bias=.29, dz=.51/8)),
        ("no offset correction, PVT 0", Err(dz=.51/8)),
        ("short window Td=150ps: bias -0.26, sigma 0.011", Err(bias=-.26, sigma=.011)),
        ("cap mismatch 5%: sigma 0.054", Err(sigma=.054)),
        ("stress: sigma 0.3", Err(sigma=.3)),
        ("stress: sigma 0.5", Err(sigma=.5)),
    ]
    rows = [("scenario", "acc")]
    for name, E in S:
        a = acc(net, x, y, E); rows.append((name, round(a, 2)))
        print(f"{a:6.2f}%  {name}", flush=True)
    csv.writer(open(f"{OUT}/scenarios.csv", "w")).writerows(rows)

def table(path):
    """Per-corner accuracy from column data: rows = corner vdd temp k v (dense input, weights=1)."""
    import pandas as pd
    df = pd.read_csv(path, sep=None, engine="python", header=None)
    if not str(df.iloc[0, 1]).replace(".", "").isdigit(): df = df.iloc[1:]
    if df.shape[1] != 5:
        sys.exit(f"expected 5 columns (corner vdd temp k v), got {df.shape[1]}: {df.iloc[0].tolist()}")
    df.columns = ["corner", "vdd", "temp", "k", "v"]
    df[["vdd", "temp", "k", "v"]] = df[["vdd", "temp", "k", "v"]].astype(float)
    nom = df[(df.corner == "tt") & (df.vdd == 1.8) & (df.temp == 27)].sort_values("k")
    ratio, kk = (nom.v / 1.8).values, nom.k.values                    # nominal V/VDD vs count
    order = np.argsort(ratio)
    net, x, y = get()
    rows = [("corner", "vdd", "temp", "max_abs_err", "acc")]
    for (c, v, t), g in df.groupby(["corner", "vdd", "temp"]):
        g = g.sort_values("k")
        dec = np.interp(g.v.values / v, ratio[order], kk[order])      # decoded float count
        etab = dec - g.k.values
        a = acc(net, x, y, Err(etab=etab, dz=.095/8))
        rows.append((c, v, t, round(float(np.abs(etab).max()), 3), round(a, 2)))
        print(f"{c} {v} {t:5.0f}  max|e|={np.abs(etab).max():.3f}  acc={a:.2f}%", flush=True)
    csv.writer(open(f"{OUT}/table_acc.csv", "w")).writerows(rows)



def pairs(path=None):
    """Unmatched column pairs (R1): W+ and W- columns get DIFFERENT errors.
    path (optional): array_pvt_out/per_run.csv from array_pvt_analysis.py -> uses the measured
    per-count corrected error at the worst array corner as a k-dependent table."""
    net, x, y = get()
    rows = [("case", "W+ error", "W- error", "acc")]
    def run(name, ep, en, Ep, En):
        a = acc(net, x, y, Err(**Ep, neg=Err(**En)))
        rows.append((name, ep, en, round(a, 2))); print(f"{a:6.2f}%  {name}   [W+: {ep} | W-: {en}]", flush=True)
    run("matched, ideal", "0", "0", {}, {})
    # 1) constant skew: one column of the pair biased, the other ideal (and the reverse)
    for b in [-1.0, -0.8, -0.6, -0.5, -0.478, -0.4, -0.3, -0.2, 0.2, 0.3, 0.4, 0.478, 0.5, 0.6]:
        run(f"skew W+ only, bias {b}", f"{b}", "0", {"bias": b}, {})
        run(f"skew W- only, bias {b}", "0", f"{b}", {}, {"bias": b})
    # 2) opposite-sign skew: pair pulled apart
    for b in [0.2, 0.3, 0.4, 0.478]:
        run(f"opposite, +/-{b}", f"{-b}", f"{+b}", {"bias": -b}, {"bias": b})
    # 3) measured k-dependent error at the worst array corner (from the R1 array run)
    if path:
        import pandas as pd
        R = pd.read_csv(path)
        wc = R.groupby(["corner","vdd","temp"]).err_corr.apply(lambda s: s.abs().max()).idxmax()
        wc = (str(wc[0]), float(wc[1]), int(wc[2]))
        g = R[(R.corner==wc[0])&(R.vdd==wc[1])&(R.temp==wc[2])]
        km = g.groupby("k").err_corr.agg(lambda s: s.loc[s.abs().idxmax()])     # worst error per k
        tab = np.interp(np.arange(9), km.index.values, km.values)                # fill missing k
        print(f"worst array corner {wc}: per-count error table", np.round(tab, 3))
        run(f"measured table {wc}, both columns (matched)", "table", "table", {"etab": tab}, {"etab": tab})
        run(f"measured table {wc} on W+ only", "table", "0", {"etab": tab}, {})
        run(f"measured table {wc} on W- only", "0", "table", {}, {"etab": tab})
        run(f"table on W+, table + sigma 0.036 (3 sigma mismatch)", "table+0.036", "0", {"etab": tab, "sigma": .036}, {"sigma": .036})
    csv.writer(open(f"{OUT}/pairs.csv", "w")).writerows(rows)
    print("wrote", f"{OUT}/pairs.csv")

if __name__ == "__main__":
    cmd = args[0] if args else "train"
    if cmd == "pairs":
        pairs(args[1] if len(args) > 1 else None)
    else:
        {"train": train, "sweep": sweep, "scenarios": scenarios}.get(cmd, lambda: table(args[1]))()
