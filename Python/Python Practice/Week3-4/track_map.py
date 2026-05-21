# track_map.py

import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2 * np.pi, 500)

# Oval-ish track with some variation to make it interesting
g_limit = 1.5
x=  np.cos(t)*40  + np.cos(2*t)*5
y = 20 * np.sin(t)
dx = np.diff(x)
dy = np.diff(y)
ddx = np.diff(dx)
ddy = np.diff(dy)
curvature = np.abs(dx[:-1] * ddy - dy[:-1] * ddx) / (dx[:-1]**2 + dy[:-1]**2)**1.5
v_max = np.sqrt(g_limit* 9.81/ curvature)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

ax1.plot(x, y, color='steelblue', linewidth=2.5)
ax1.plot(x[0], y[0], 'go', markersize=10, label='Start/Finish')
ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')
ax1.set_title('FSAE Autocross Track Layout')
ax1.legend()
ax1.axis('equal')
ax1.grid(True, alpha=0.3)

ax2.plot(curvature, color='purple', linewidth=2)
ax2.set_xlabel('Track Position (index)', fontsize=12)
ax2.set_ylabel('Curvature (1/m)', fontsize=12)
ax2.set_title('Track Curvature vs Position', fontsize=13)
ax2.grid(True, alpha=0.3)
plt.savefig('curvature.png', dpi=150)

ax3.plot(v_max, color='red', linewidth=2)
ax3.set_xlabel('Track Position (index)', fontsize=12)
ax3.set_ylabel('Maximum Velocity (m/s)', fontsize=12)
ax3.set_title('Maximum Velocity vs Position', fontsize=13)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()