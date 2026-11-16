#!/usr/bin/env python3
"""SNM from one half-cell VTC (ngspice wrdata: columns x, y). Symmetric cell assumed:
the butterfly is the VTC and its mirror about y = x. Seevinck's method: rotate by 45 deg,
SNM = (smaller lobe's largest separation along v) / sqrt(2)."""
import sys, numpy as np
d = np.loadtxt(sys.argv[1]); x, y = d[:, 0], d[:, -1]
u = (x - y) / np.sqrt(2); v = (x + y) / np.sqrt(2)          # VTC is decreasing -> u increasing
o = np.argsort(u); u, v = u[o], v[o]
ug = np.linspace(max(u.min(), -u.max()), min(u.max(), -u.min()), 4001)
va = np.interp(ug, u, v); vb = np.interp(-ug, u, v)       # mirror curve: (u,v) -> (-u,v)
diff = va - vb
snm = min(diff.max(), (-diff).max()) / np.sqrt(2)
print(f"SNM = {snm*1000:.1f} mV  (lobes {diff.max()/np.sqrt(2)*1000:.1f} / {(-diff).max()/np.sqrt(2)*1000:.1f} mV)")
