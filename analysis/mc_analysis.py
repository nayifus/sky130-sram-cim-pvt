#!/usr/bin/env python3
"""Analyse Monte Carlo runs of the 8-cell charge-domain CIM column.

Input : one or more  label=file:vdd  arguments. Each file has rows 'sample k v_cl'.
        The FIRST argument is the calibration reference (nominal run).
Output: mc_out/ next to the first file: mc_summary.csv, per_count_table.csv, fig_mc.png

Decoder ("nomratio"): two-point calibration taken from the reference run's mean
voltages, applied to V/VDD so the thresholds follow the supply.

Usage : python3 mc_analysis.py nom=mc_nom.csv:1.8 ss=mc_ss.csv:1.62 ss150=mc_ss_td150.csv:1.62
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

N = 8
if len(sys.argv) < 2:
    sys.exit(__doc__)

runs = []
for a in sys.argv[1:]:
    label, rest = a.split("=", 1)
    path, vdd = rest.rsplit(":", 1)
    df = pd.read_csv(path, sep=r"\s+", header=None, names=["s", "k", "v"],
                     engine="python", on_bad_lines="skip")
    df = df.apply(pd.to_numeric, errors="coerce").dropna().drop_duplicates(["s", "k"], keep="last")
    M = df.pivot(index="s", columns="k", values="v").dropna()
    if list(M.columns) != list(range(N + 1)):
        sys.exit(f"{path}: needs k = 0..{N} for every sample")
    runs.append((label, float(vdd), M, os.path.abspath(path)))

out = os.path.join(os.path.dirname(runs[0][3]), "mc_out")
os.makedirs(out, exist_ok=True)

# reference calibration, in units of VDD
lab0, vdd0, M0, _ = runs[0]
R0, R8 = M0[0].mean() / vdd0, M0[N].mean() / vdd0
kk = np.arange(N + 1)

summ, tables, errs = [], [], {}
for label, vdd, M, _ in runs:
    V = M.to_numpy()
    E = N * (R0 - V / vdd) / (R0 - R8) - kk        # decoded - true, counts
    errs[label] = E
    sd_mv = V.std(axis=0, ddof=1) * 1e3
    # per-die straight-line fit v = a - g*k  (does each die keep its own gain and offset?)
    fits = np.array([np.polyfit(kk, v, 1) for v in V])
    corr = np.corrcoef(V[:, 0], V[:, N])[0, 1]     # same die across k  ->  strongly positive
    summ.append(dict(run=label, vdd=vdd, samples=len(V),
                     sigma_mv_min=sd_mv.min(), sigma_mv_max=sd_mv.max(),
                     sigma_counts_max=E.std(axis=0, ddof=1).max(),
                     worst_abs_err_counts=np.abs(E).max(),
                     mean_err_counts_maxabs=np.abs(E.mean(axis=0)).max(),
                     misdecoded=int((np.rint(E + kk) != kk).sum()),
                     gain_mean=-fits[:, 0].mean() / (vdd / N), gain_sd=fits[:, 0].std(ddof=1) / (vdd / N),
                     corr_k0_k8=corr))
    for k in kk:
        tables.append(dict(run=label, k=int(k), v_mean=V[:, k].mean(), v_sd_mv=sd_mv[k],
                           err_mean_counts=E[:, k].mean(), err_sd_counts=E[:, k].std(ddof=1)))

S = pd.DataFrame(summ)
T = pd.DataFrame(tables)
S.to_csv(os.path.join(out, "mc_summary.csv"), index=False)
T.to_csv(os.path.join(out, "per_count_table.csv"), index=False)

pd.set_option("display.width", 170)
print(f"Calibration from '{lab0}': V(k=0)/VDD = {R0:.5f}, V(k=8)/VDD = {R8:.5f}\n")
print(S.round(4).to_string(index=False))
print("\nPer-count decode error (counts), mean +/- sd:")
w = T.pivot(index="k", columns="run", values=["err_mean_counts", "err_sd_counts"])
for label, *_ in runs:
    print(f"  {label}: " + "  ".join(f"k{k}:{w['err_mean_counts'][label][k]:+.3f}/{w['err_sd_counts'][label][k]:.3f}" for k in kk))

colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
for i, (label, vdd, M, _) in enumerate(runs):
    ax[0].plot(kk, M.std(axis=0, ddof=1) * 1e3, "o-", color=colors[i], label=label)
    e = errs[label]
    ax[1].errorbar(kk + (i - 1) * 0.12, e.mean(axis=0), yerr=3 * e.std(axis=0, ddof=1), fmt="o", ms=4,
                   color=colors[i], capsize=3, label=label)
ax[0].set(xlabel="k", ylabel="sigma of V_CL (mV)", title="Spread across Monte Carlo samples")
ax[0].legend()
ax[1].axhspan(-0.5, 0.5, color="#1b9e77", alpha=0.12)
ax[1].set(xlabel="k", ylabel="decoded - true (counts)",
          title="Decode error, mean +/- 3 sigma (green = correct)")
ax[1].legend()
fig.tight_layout()
fig.savefig(os.path.join(out, "fig_mc.png"), dpi=150)
print(f"\nSaved to {out}: mc_summary.csv, per_count_table.csv, fig_mc.png")
