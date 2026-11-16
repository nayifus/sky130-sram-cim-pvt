#!/usr/bin/env python3
"""Analyse the PVT sweep of the 8-cell charge-domain CIM column.

Input : pvt_results.csv, whitespace separated, one row per run:
        corner vdd temp k v_cl
Output: PNG figures + CSV tables in the folder 'pvt_out' (next to the input file).

Usage : python3 pvt_analysis.py pvt_results.csv
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

N = 8                      # cells per column
NOM = ("tt", 1.8, 27.0)    # nominal condition used to calibrate the fixed decoder

fn = sys.argv[1] if len(sys.argv) > 1 else "pvt_results.csv"
out = os.path.join(os.path.dirname(os.path.abspath(fn)), "pvt_out")
os.makedirs(out, exist_ok=True)

# ---------------------------------------------------------------- load
df = pd.read_csv(fn, sep=r"\s+", header=None, engine="python",
                 names=["corner", "vdd", "temp", "k", "v"], on_bad_lines="skip")
for c in ["vdd", "temp", "k", "v"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna().drop_duplicates(["corner", "vdd", "temp", "k"], keep="last")
df["k"] = df["k"].astype(int)
df = df.sort_values(["corner", "vdd", "temp", "k"]).reset_index(drop=True)

conds = df.groupby(["corner", "vdd", "temp"]).k.nunique()
bad = conds[conds != N + 1]
if len(bad):
    print("WARNING: these conditions do not have all 9 k values and are skipped:")
    print(bad)
    keep = conds[conds == N + 1].index
    df = df[df.set_index(["corner", "vdd", "temp"]).index.isin(keep)].reset_index(drop=True)

nom = df[(df.corner == NOM[0]) & np.isclose(df.vdd, NOM[1]) & np.isclose(df.temp, NOM[2])]
if len(nom) != N + 1:
    sys.exit("The nominal condition (tt, 1.8 V, 27 C) is missing from the file.")
V0_NOM = float(nom[nom.k == 0].v.iloc[0])
V8_NOM = float(nom[nom.k == N].v.iloc[0])
print(f"Nominal calibration: V(k=0) = {V0_NOM:.4f} V, V(k=8) = {V8_NOM:.4f} V, "
      f"step = {(V0_NOM - V8_NOM) / N:.4f} V (ideal {NOM[1] / N:.4f} V)")

# ---------------------------------------------------------------- decoders
# ideal : thresholds from the ideal line VDD*(1-k/N), following the actual supply
# nomcal: fixed absolute thresholds from the nominal two-point calibration
# nomratio: nominal two-point calibration applied to V/VDD, so the thresholds scale with the supply
#          (in hardware this is a reference that tracks VDD, e.g. a replica column or a divider)
# percal: two-point calibration redone at every condition
df["k_ideal"] = N * (1 - df.v / df.vdd)
df["k_nomcal"] = N * (V0_NOM - df.v) / (V0_NOM - V8_NOM)
R0_NOM, R8_NOM = V0_NOM / NOM[1], V8_NOM / NOM[1]
df["k_nomratio"] = N * (R0_NOM - df.v / df.vdd) / (R0_NOM - R8_NOM)
g = df.groupby(["corner", "vdd", "temp"])
v0 = g.v.transform(lambda s: s.iloc[0])
v8 = g.v.transform(lambda s: s.iloc[-1])
df["k_percal"] = N * (v0 - df.v) / (v0 - v8)
DEC = ["ideal", "nomcal", "nomratio", "percal"]
for d in DEC:
    df["e_" + d] = df["k_" + d] - df.k
    df["w_" + d] = np.clip(np.rint(df["k_" + d]), 0, N) != df.k

# ---------------------------------------------------------------- per-condition summary
rows = []
for (c, vdd, t), s in df.groupby(["corner", "vdd", "temp"]):
    s = s.sort_values("k")
    a, b = np.polyfit(s.k, s.e_nomcal, 1)       # e_k = a*k + b under the fixed decoder
    r = dict(corner=c, vdd=vdd, temp=t,
             v_k0=s.v.iloc[0], v_k8=s.v.iloc[-1],
             gain=(s.v.iloc[0] - s.v.iloc[-1]) / vdd,   # ideal = 1
             fit_a=a, fit_b=b)
    for d in DEC:
        r["maxerr_" + d] = s["e_" + d].abs().max()
        r["wrong_" + d] = int(s["w_" + d].sum())
    rows.append(r)
summ = pd.DataFrame(rows)
summ.to_csv(os.path.join(out, "condition_summary.csv"), index=False)

# per-count error table for the DNN noise model (fixed nominal decoder, all conditions)
pc = df.groupby("k").e_nomcal.agg(mean="mean", std="std", min="min", max="max").reset_index()
pc.to_csv(os.path.join(out, "per_count_error_table.csv"), index=False)

# ---------------------------------------------------------------- printed report
n = len(summ)
print(f"\n{n} conditions analysed ({summ.corner.nunique()} corners)")
for d in DEC:
    ok = int((summ["wrong_" + d] == 0).sum())
    print(f"  decoder {d:7s}: {ok:2d}/{n} conditions decode all 9 counts correctly, "
          f"worst error {summ['maxerr_' + d].max():.2f} counts")

pd.set_option("display.width", 160)
print("\nWorst 8 conditions for the fixed nominal decoder:")
print(summ.sort_values("maxerr_nomcal", ascending=False).head(8)[
    ["corner", "vdd", "temp", "gain", "v_k0", "maxerr_nomcal", "wrong_nomcal", "maxerr_nomratio", "wrong_nomratio", "maxerr_percal"]
].round(3).to_string(index=False))

print("\nPer-count error of the fixed nominal decoder over all conditions (counts):")
print(pc.round(3).to_string(index=False))

# ---------------------------------------------------------------- figures
colors = {"tt": "#1b9e77", "ss": "#d95f02", "ff": "#7570b3", "sf": "#e7298a", "fs": "#66a61e"}

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
nomrows = df[np.isclose(df.vdd, NOM[1]) & np.isclose(df.temp, NOM[2])]
for c, s in nomrows.groupby("corner"):
    ax[0].plot(s.k, s.v, "o-", ms=4, color=colors.get(c), label=c)
ax[0].plot(range(N + 1), [NOM[1] * (1 - k / N) for k in range(N + 1)], "k--", lw=1, label="ideal")
ax[0].set(title="Column voltage vs k, all corners at 1.8 V, 27 C", xlabel="k", ylabel="V_CL (V)")
ax[0].legend()
for (c, vdd, t), s in df.groupby(["corner", "vdd", "temp"]):
    ax[1].plot(s.k, s.v / vdd, color=colors.get(c), alpha=0.35, lw=1)
ax[1].plot(range(N + 1), [1 - k / N for k in range(N + 1)], "k--", lw=1)
ax[1].set(title="V_CL / VDD, all 45 conditions", xlabel="k", ylabel="V_CL / VDD")
fig.tight_layout()
fig.savefig(os.path.join(out, "fig1_staircases.png"), dpi=150)

fig, ax = plt.subplots(1, 4, figsize=(16, 4.2), sharey=True)
worst = summ.sort_values("maxerr_nomcal", ascending=False).head(3)
for i, d in enumerate(DEC):
    for (c, vdd, t), s in df.groupby(["corner", "vdd", "temp"]):
        ax[i].plot(s.k, s["e_" + d], color="0.7", lw=0.8)
    ax[i].axhspan(-0.5, 0.5, color="#1b9e77", alpha=0.12)
    ax[i].set(title=f"decoder: {d}", xlabel="k")
ax[0].set_ylabel("decoded - true (counts)")
for _, r in worst.iterrows():
    s = df[(df.corner == r.corner) & np.isclose(df.vdd, r.vdd) & np.isclose(df.temp, r.temp)]
    ax[1].plot(s.k, s.e_nomcal, lw=1.8, label=f"{r.corner} {r.vdd:g} V {r.temp:g} C")
ax[1].legend(fontsize=8)
fig.suptitle("Decoding error vs k (green band = decodes correctly)")
fig.tight_layout()
fig.savefig(os.path.join(out, "fig2_errors.png"), dpi=150)

# heatmaps: wrong counts for the two fixed-threshold decoders
cols = sorted(set(zip(summ.vdd, summ.temp)))
rows_ = [r for r in ["tt", "ss", "ff", "sf", "fs"] if r in set(summ.corner)]
fig, axs = plt.subplots(2, 1, figsize=(11, 6.2))
for ax, d, ttl in [(axs[0], "nomcal", "thresholds fixed at nominal (absolute volts)"),
                   (axs[1], "nomratio", "nominal thresholds scaled with VDD (ratio)")]:
    M = np.full((len(rows_), len(cols)), np.nan)
    for _, r in summ.iterrows():
        M[rows_.index(r.corner), cols.index((r.vdd, r.temp))] = r["wrong_" + d]
    im = ax.imshow(M, cmap="Reds", vmin=0, vmax=9, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([f"{v:g} V\n{t:g} C" for v, t in cols], fontsize=8)
    ax.set_yticks(range(len(rows_)))
    ax.set_yticklabels(rows_)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if not np.isnan(M[i, j]):
                ax.text(j, i, int(M[i, j]), ha="center", va="center", fontsize=9)
    ax.set_title("Misdecoded counts (out of 9): " + ttl, fontsize=10)
    fig.colorbar(im, ax=ax, pad=0.01)
fig.tight_layout()
fig.savefig(os.path.join(out, "fig3_wrong_counts_heatmap.png"), dpi=150)

print(f"\nSaved to {out}: condition_summary.csv, per_count_error_table.csv, "
      f"fig1_staircases.png, fig2_errors.png, fig3_wrong_counts_heatmap.png")
