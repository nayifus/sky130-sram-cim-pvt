#!/usr/bin/env python3
"""Capacitor-mismatch Monte Carlo: measured sigma(V_CL) vs k against a first-order model.

Usage:
  python3 cap_analysis.py VDD NOM.csv BASE.csv  CAP_A.csv:0.01  CAP_B.csv:0.05 ...
    VDD      supply of the BASE/CAP runs (e.g. 1.62)
    NOM.csv  nominal MC run (calibration reference, VDD 1.8; rows 'sample k v')
    BASE.csv same corner with csig=0 (transistor mismatch only)
    CAP_x    runs with csig>0, written as file:csig

Model: V_CL = VDD*(1 - sum(C_discharged)/(sum(C_all)+Cpar)); Cpar/C is taken from the measured gain.
Outputs (cap_out/): cap_sigma_table.csv, fig_cap.png ; prints decode-error stats.
"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if len(sys.argv) < 5:
    sys.exit(__doc__)

N = 8
vdd = float(sys.argv[1])

def load(p):
    d = pd.read_csv(p, sep=r"\s+", header=None, names=["s", "k", "v"], engine="python", on_bad_lines="skip")
    d = d.apply(pd.to_numeric, errors="coerce").dropna().drop_duplicates(["s", "k"], keep="last")
    M = d.pivot(index="s", columns="k", values="v").dropna()
    if list(M.columns) != list(range(N + 1)):
        sys.exit(f"{p}: needs k = 0..{N} for every sample")
    return M

nom, base = load(sys.argv[2]), load(sys.argv[3])
caps = []
for a in sys.argv[4:]:
    p, cs = a.rsplit(":", 1)
    caps.append((os.path.basename(p), float(cs), load(p)))

out = os.path.join(os.path.dirname(os.path.abspath(sys.argv[3])), "cap_out")
os.makedirs(out, exist_ok=True)
k = np.arange(N + 1)
gain = -np.polyfit(k, caps[0][2].mean().values, 1)[0] / (vdd / N)
cpar = N * (1 / gain - 1)
B = N + cpar
f = k / B
lsb = gain * vdd / N * 1e3
model = lambda cs: vdd * cs * np.sqrt(k * (1 - f) ** 2 + (N - k) * f ** 2) / B * 1e3
print(f"gain {gain:.4f}   Cpar/C {cpar:.2f}   1 count = {lsb:.1f} mV\n")

tab = pd.DataFrame({"k": k, "base_mV": base.std().values * 1e3})
for name, cs, M in caps:
    tab[f"{cs:g}_sim_mV"] = M.std().values * 1e3
    tab[f"{cs:g}_model_mV"] = model(cs)
tab.to_csv(os.path.join(out, "cap_sigma_table.csv"), index=False)
pd.set_option("display.width", 170)
print(tab.round(2).to_string(index=False))

R0, R8 = nom[0].mean() / 1.8, nom[N].mean() / 1.8
print("\nDecode error (counts), nominal VDD-tracking calibration:")
for name, M in [("base", base)] + [(n, m) for n, _, m in caps]:
    E = N * (R0 - M.values / vdd) / (R0 - R8) - k
    print(f"  {name:<22} worst |err| {abs(E).max():.3f}   max sd {E.std(0, ddof=1).max():.3f}"
          f"   misdecoded {(np.rint(E + k) != k).sum()} / {E.size}   max |mean bias| {abs(E.mean(0)).max():.3f}")

cols = ["#1b9e77", "#d95f02", "#e7298a", "#66a61e"]
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.plot(k, tab.base_mV, "^-", color="#7570b3", label="no cap mismatch (transistors only)")
for i, (name, cs, M) in enumerate(caps):
    c = cols[i % len(cols)]
    ax.plot(k, tab[f"{cs:g}_sim_mV"], "o-", color=c, label=f"{cs*100:g} % cap sigma (sim)")
    ax.plot(k, tab[f"{cs:g}_model_mV"], "--", color=c, label=f"{cs*100:g} % (model)")
ax.set(xlabel="k (cells discharging)", ylabel="sigma of V_CL (mV)", title="Capacitor mismatch: sigma(V_CL) vs k")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(out, "fig_cap.png"), dpi=150)
print(f"\nSaved to {out}: cap_sigma_table.csv, fig_cap.png")
