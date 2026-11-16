#!/usr/bin/env python3
"""Per-row input-dependent offset of the CIM column over PVT.

Usage: python3 delta_analysis.py delta_results.csv pvt_results.csv
  delta_results.csv rows: corner vdd temp iv v   (iv=1: all inputs 1, iv=0: all inputs 0; weights all 0)
  pvt_results.csv   rows: corner vdd temp k v    (corrected-timing PVT sweep)
Outputs delta_out/delta_summary.csv and prints the spread and the residual after a fixed correction.
"""
import os, sys
import numpy as np
import pandas as pd

if len(sys.argv) != 3:
    sys.exit(__doc__)
d = pd.read_csv(sys.argv[1], sep=r"\s+", header=None, names=["c", "v", "t", "i", "x"])
p = pd.read_csv(sys.argv[2], sep=r"\s+", header=None, names=["c", "v", "t", "k", "x"])
rows = []
for (c, v, t), g in d.groupby(["c", "v", "t"]):
    V1 = g[g.i == 1].x.iloc[0]
    V0 = g[g.i == 0].x.iloc[0]
    q = p[(p.c == c) & (p.v == v) & (p.t == t)].set_index("k").x
    cnt = (q[0] - q[8]) / 8
    dl = (V0 - V1) / 8
    rows.append(dict(corner=c, vdd=v, temp=t, V_allones=V1, V_allzero=V0, delta_mV=dl * 1e3, count_mV=cnt * 1e3,
                     delta_counts=dl / cnt, allzero_counts=8 * dl / cnt, delta_mV_per_V=dl / v * 1e3,
                     check_vs_pvt_mV=(V1 - q[0]) * 1e3))
r = pd.DataFrame(rows)
nom = r[(r.corner == "tt") & (r.vdd == 1.8) & (r.temp == 27)].iloc[0]
r["resid_fixed_counts"] = 8 * (r.delta_counts - nom.delta_counts)
r["resid_vddscaled_counts"] = 8 * (r.delta_mV_per_V - nom.delta_mV_per_V) * r.vdd / r.count_mV
out = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "delta_out")
os.makedirs(out, exist_ok=True)
r.to_csv(os.path.join(out, "delta_summary.csv"), index=False)
pd.set_option("display.width", 200)
print(r.round(3).sort_values("allzero_counts", ascending=False).to_string(index=False))
print(f"\nmax |all-ones - PVT k=0| = {r.check_vs_pvt_mV.abs().max():.2f} mV (sanity: should be ~1 mV)")
print(f"offset per zero-input row: {r.delta_mV.min():.2f} - {r.delta_mV.max():.2f} mV = {r.delta_counts.min():.4f} - {r.delta_counts.max():.4f} counts")
print(f"all 8 inputs zero, uncorrected: {r.allzero_counts.min():.3f} - {r.allzero_counts.max():.3f} counts")
print(f"nominal: {nom.delta_mV:.2f} mV = {nom.delta_counts:.4f} counts per zero row")
print(f"residual after fixed {nom.delta_counts:.4f} counts/row correction: worst {r.resid_fixed_counts.abs().max():.3f} counts")
print(f"residual after VDD-scaled mV correction:            worst {r.resid_vddscaled_counts.abs().max():.3f} counts")
print(f"\nSaved to {out}")
