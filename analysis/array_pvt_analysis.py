#!/usr/bin/env python3
"""R1 revision: offset correction on the 8x4 array across 45 PVT conditions and 12 input patterns.
Usage:  python3 array_pvt_analysis.py array_pvt.csv
Input rows: corner vdd temp pattern V_CL0 V_CL1 V_CL2 V_CL3   (from tb_array_pvt.spice)
Decoder: supply-tracking (V/VDD through the nominal tt/1.8V/27C column calibration), then round.
Correction: add delta * (number of inactive rows), delta in counts.
Writes array_pvt_out/: per_run.csv, by_condition.csv, by_pattern.csv, fig_array_pvt.png
"""
import sys, os, numpy as np, pandas as pd
OUT = "array_pvt_out"; os.makedirs(OUT, exist_ok=True)

# nominal column calibration (tt, 1.8 V, 27 C, all rows active), k = 0..8
VNOM = np.array([1.75211, 1.56384, 1.37376, 1.18311, 0.994392, 0.807055, 0.616703, 0.423891, 0.231415])
RNOM = VNOM / 1.8
DELTA = 0.0539          # counts per inactive row at nominal (0.08201 V / 8 / 0.19009 V)

# weights W[row 0..7, col 0..3] exactly as in the testbench
W = np.array([[1,1,1,0],[1,1,0,1],[1,1,1,1],[1,1,0,1],[1,0,1,1],[1,0,0,1],[1,0,1,0],[1,0,0,0]])

def bits(p): return np.array([(int(p) >> i) & 1 for i in range(8)])   # in1 = bit 0

def decode_ext(v, vdd):
    """linear extrapolation outside the calibrated range (keeps sign of errors near k=0 and 8)"""
    r = v / vdd; slope = (RNOM[0] - RNOM[-1]) / 8
    if r > RNOM[0]:  return -(r - RNOM[0]) / slope
    if r < RNOM[-1]: return 8 + (RNOM[-1] - r) / slope
    return float(np.interp(-r, -RNOM, np.arange(9.0)))

df = pd.read_csv(sys.argv[1], sep=r"\s+", header=None, names=["corner","vdd","temp","pat","v0","v1","v2","v3"])
rows = []
for _, r in df.iterrows():
    x = bits(r.pat); nz = 8 - x.sum(); ktrue = x @ W
    for c in range(4):
        kh = decode_ext(r[f"v{c}"], r.vdd)
        rows.append(dict(corner=r.corner, vdd=r.vdd, temp=r.temp, pat=int(r.pat), col=c, nz=nz, k=int(ktrue[c]),
                         err_raw=kh - ktrue[c],
                         err_corr=kh + DELTA * nz - ktrue[c],                      # step scaled with VDD (ratio decoding)
                         err_corr_fixedV=kh + DELTA * nz * 1.8 / r.vdd - ktrue[c]))  # step fixed in volts
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/per_run.csv", index=False)
a = lambda s: s.abs().max()
bc = R.groupby(["corner","vdd","temp"]).agg(max_raw=("err_raw",a), max_corr=("err_corr",a), max_corr_fixedV=("err_corr_fixedV",a)).reset_index()
bp = R.groupby(["pat","nz"]).agg(max_raw=("err_raw",a), max_corr=("err_corr",a)).reset_index()
bc.round(3).to_csv(f"{OUT}/by_condition.csv", index=False); bp.round(3).to_csv(f"{OUT}/by_pattern.csv", index=False)

n = len(R); print(f"{len(df)} runs, {n} column readouts, {R.groupby(['corner','vdd','temp']).ngroups} conditions, {R.pat.nunique()} patterns")
for col, name in [("err_raw","uncorrected"),("err_corr","corrected (VDD-scaled step)"),("err_corr_fixedV","corrected (fixed-volt step)")]:
    e = R[col]; w = R.loc[e.abs().idxmax()]
    print(f"{name:30s} max|err| {e.abs().max():.3f}  mean|err| {e.abs().mean():.3f}  misdecodes {(e.abs()>0.5).sum()}/{n}"
          f"   worst: {w.corner} {w.vdd} V {w.temp:.0f} C pat {w.pat} col {w.col} (k={w.k}, nz={w.nz})")
print("\nworst corrected error by input pattern:"); print(bp.sort_values("nz").round(3).to_string(index=False))

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    corners = [c for c in ["tt","ss","sf","fs","ff"] if c in set(bc.corner)]
    cols = [(v,t) for v in sorted(bc.vdd.unique()) for t in sorted(bc.temp.unique())]
    M = np.full((len(corners), len(cols)), np.nan)
    for i,c in enumerate(corners):
        for j,(v,t) in enumerate(cols):
            s = bc[(bc.corner==c)&(bc.vdd==v)&(bc.temp==t)]
            if len(s): M[i,j] = s.max_corr.iloc[0]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.2), gridspec_kw={"width_ratios":[1.6,1]})
    im = ax[0].imshow(M, cmap="Blues", vmin=0, vmax=0.5, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if not np.isnan(M[i,j]): ax[0].text(j, i, f"{M[i,j]:.2f}", ha="center", va="center", fontsize=7, color="white" if M[i,j]>0.25 else "black")
    ax[0].set_yticks(range(len(corners))); ax[0].set_yticklabels(corners)
    ax[0].set_xticks(range(len(cols))); ax[0].set_xticklabels([f"{v}V\n{t:.0f}C" for v,t in cols], fontsize=7)
    ax[0].set_title("Array, corrected: max |error| over 12 patterns x 4 columns (counts)", fontsize=8)
    plt.colorbar(im, ax=ax[0], fraction=0.03)
    ax[1].scatter(R.nz + np.random.uniform(-.15,.15,n), R.err_raw, s=4, c="0.6", label="uncorrected")
    ax[1].scatter(R.nz + np.random.uniform(-.15,.15,n), R.err_corr, s=4, c="tab:blue", label="corrected")
    ax[1].axhline(0.5, ls="--", c="r", lw=.8); ax[1].axhline(-0.5, ls="--", c="r", lw=.8)
    ax[1].set_xlabel("inactive rows n_z"); ax[1].set_ylabel("decode error (counts)"); ax[1].legend(fontsize=7)
    plt.tight_layout(); plt.savefig(f"{OUT}/fig_array_pvt.png", dpi=200); print(f"\nwrote {OUT}/fig_array_pvt.png")
except Exception as ex:
    print("plot skipped:", ex)
