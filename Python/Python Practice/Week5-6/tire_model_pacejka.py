# NOTE (2026-07-11): this is an early standalone demo (placeholder B/C/D/E,
# D=2800/3000/3200N light/medium/heavy). It was NEVER the number used in the
# real lap sim -- the real TTC-fit tire model (B=20.85, C=1.411, D=4180, E=-1.027)
# lives in the canonical Week3-4/lap_sim.py. Kept for history / load-sensitivity
# demo value only.
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

alpha = np.linspace(-15, 15, 500)
alpha_rad = np.deg2rad(alpha)
B = 10.0
C = 1.9
light_D = 2800
medium_D = 3000
heavy_D = 3200
E = -1.5

for D in [light_D, medium_D, heavy_D]:
    Fy = D * np.sin(C * np.arctan(B * alpha_rad - E * (B * alpha_rad - np.arctan(B * alpha_rad))))  
    if D == light_D:
        fy_light = Fy
    elif D == medium_D:
        fy_medium = Fy
    else:
        fy_heavy = Fy
        
fy_linear = 800 * alpha
fy_linear = np.clip(fy_linear, -2800, 2800)

plt.plot(alpha, fy_light, label="Light Load")
plt.plot(alpha, fy_medium, label="Medium Load")
plt.plot(alpha, fy_heavy, label="Heavy Load")
plt.plot(alpha, fy_linear, label="Linear")
plt.xlabel("Slip Angle (degrees)")
plt.ylabel("Lateral Force (N)")
plt.title("Tire Lateral Force vs Slip Angle")
plt.axvline(x=3, color='red', linestyle='--', alpha=0.6, label='Linear limit (~3°)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
