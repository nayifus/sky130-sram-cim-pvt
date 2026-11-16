#!/usr/bin/env python3
"""Analyse the compute-window (T_d) sweep of the CIM column.

Input : td_results.csv, whitespace separated, one row per run:
        corner vdd temp td_seconds k v_cl        (k is 0 or 8)
Output: td_out/ next to the input: td_summary.csv and fig_td.png

For every (corner, vdd, temp) it reports
  tau_ps : discharge time constant fitted from the missing signal vs T_d
  td_min_ps : shortest T_d for which k=0 and k=8 still decode within +-0.5 counts
              using the VDD-scaled nominal calibration (tt, 1.8 V, 27 C, longest T_d)
Usage : python3 td_analysis.py td_results.csv
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

N = 8
NOM = ("tt", 1.8, 27.0)
fn = sys.argv[1] if len(sys.argv) > 1 else "td_results.csv"
out = os.path.join(os.path.dirname(os.path.abspath(fn)), "td_out")
os.makedirs(out, exist_ok=True)

df = pd.read_csv(fn, sep=r"\s+", header=None, engine="python",
                 names=["corner", "vdd", "temp", "td", "k", "v"], on_bad_lines="skip")
for c in ["vdd", "temp", "td", "k", "v"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna().drop_duplicates(["corner", "vdd", "temp", "td", "k"], keep="last")
df["k"] = df["k"].astype(int)

wide = df.pivot_table(index=["corner", "vdd", "temp", "td"], columns="k", values="v").reset_index()
if 0 not in wide or N not in wide:
    sys.exit("The file needs both k=0 and k=8 rows.")
wide = wide.dropna(subset=[0, N]).rename(columns={0: "v0", N: "v8"})

# nominal calibration: tt, 1.8 V, 27 C at the longest T_d
nomrows = wide[(wide.corner == NOM[0]) & np.isclose(wide.vdd, NOM[1]) & np.isclose(wide.temp, NOM[2])]
if nomrows.empty:
    sys.exit("Need the nominal condition (tt, 1.8 V, 27 C) in the file.")
ref = nomrows.sort_values("td").iloc[-1]
R0, R8 = ref.v0 / NOM[1], ref.v8 / NOM[1]
print(f"Nominal reference at T_d = {ref.td * 1e9:.2f} ns: V(k=0) = {ref.v0:.4f} V, V(k=8) = {ref.v8:.4f} V")

wide["e0"] = N * (R0 - wide.v0 / wide.vdd) / (R0 - R8)
wide["e8"] = N * (R0 - wide.v8 / wide.vdd) / (R0 - R8) - N
wide["maxerr"] = wide[["e0", "e8"]].abs().max(axis=1)

rows = []
for (c, vdd, t), s in wide.groupby(["corner", "vdd", "temp"]):
    s = s.sort_values("td")
    span = s.v0 - s.v8
    eps = 1 - span / span.iloc[-1]            # fraction of the signal missing vs the longest window
    m = (eps > 0.005) & (eps < 0.8) & (s.td < s.td.iloc[-1])
    tau = np.nan
    if m.sum() >= 2:
        slope, _ = np.polyfit(s.td[m], np.log(eps[m]), 1)
        if slope < 0:
            tau = -1 / slope
    ok = (s.maxerr < 0.5).to_numpy()
    td_min = np.nan
    for i in range(len(s) - 1, -1, -1):        # walk down from the longest window
        if ok[i]:
            td_min = s.td.iloc[i]
        else:
            break
    rows.append(dict(corner=c, vdd=vdd, temp=t, tau_ps=tau * 1e12, td_min_ps=td_min * 1e12,
                     err_at_shortest=s.maxerr.iloc[0]))
summ = pd.DataFrame(rows).sort_values("td_min_ps", ascending=False)
summ.to_csv(os.path.join(out, "td_summary.csv"), index=False)

pd.set_option("display.width", 140)
print("\nConditions sorted from slowest to fastest (td_min = shortest safe compute window):")
print(summ.round(2).to_string(index=False))
if summ.td_min_ps.notna().any():
    w = summ.iloc[0]
    print(f"\nWorst case: {w.corner}, {w.vdd:g} V, {w.temp:g} C needs T_d >= {w.td_min_ps:.0f} ps "
          f"(tau = {w.tau_ps:.0f} ps). Pick the real T_d with margin above this.")

colors = {"tt": "#1b9e77", "ss": "#d95f02", "ff": "#7570b3", "sf": "#e7298a", "fs": "#66a61e"}
fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
for (c, vdd, t), s in wide.groupby(["corner", "vdd", "temp"]):
    s = s.sort_values("td")
    lab = f"{c} {vdd:g} V {t:g} C"
    ax[0].plot(s.td * 1e12, s.maxerr, "o-", ms=3, lw=1.3, color=colors.get(c, "k"), alpha=0.8, label=lab)
    span = s.v0 - s.v8
    ax[1].plot(s.td * 1e12, 1 - span / span.iloc[-1], "o-", ms=3, lw=1.3, color=colors.get(c, "k"), alpha=0.8)
ax[0].axhline(0.5, color="k", ls="--", lw=1)
ax[0].set(xscale="log", yscale="log", xlabel="T_d (ps)", ylabel="worst decode error (counts)",
          title="Decode error vs compute window (limit = 0.5)")
ax[0].legend(fontsize=6, ncol=2)
ax[1].set(xscale="log", yscale="log", ylim=(1e-4, 1.5), xlabel="T_d (ps)",
          ylabel="fraction of signal missing", title="Incomplete discharge")
fig.tight_layout()
fig.savefig(os.path.join(out, "fig_td.png"), dpi=150)
print(f"\nSaved to {out}: td_summary.csv, fig_td.png")
