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


a_max = 10 # m/s^2
a_brake = 15 # m/s^2
ds = 1      # approximate distance per index step

v_forward = v_max.copy()
v_backward = v_max.copy()

for i in range(1, len(v_forward)):
    v_possiblefwd = np.sqrt(v_forward[i-1]**2 + 2 * a_max * ds)
    v_forward[i] = min(v_possiblefwd, v_max[i])

for i in range(len(v_forward)-2, -1, -1):
    v_possiblebwd = np.sqrt(v_backward[i+1]**2 + 2 * a_brake * ds)
    v_backward[i] = min(v_possiblebwd, v_max[i])

v_final = np.minimum(v_forward, v_backward)


fig, (ax1, ax2, ax3, ax4,ax5,ax6) = plt.subplots(1, 6, figsize=(16, 5))

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

ax4.plot(v_max, color='red', linewidth=2, label='Grip limit', alpha=0.5)
ax4.plot(v_forward, color='blue', linewidth=2, label='Forward pass')
ax4.set_xlabel("Track Position (index)", fontsize=12)
ax4.set_ylabel("Forward Velocity (m/s)", fontsize=12)
ax4.set_title('Actual Forward Velocity vs Position', fontsize=13)
ax4.grid(True, alpha=0.3)
ax4.legend()

ax5.plot(v_max, color='red', linewidth=2, label='Grip limit', alpha=0.5)
ax5.plot(v_final, color='green', linewidth=2, label='backward pass')
ax5.set_xlabel("Track Position (index)", fontsize=12)
ax5.set_ylabel("Backward Velocity (m/s)", fontsize=12)
ax5.set_title('Actual backward Velocity vs Position', fontsize=13)
ax5.grid(True, alpha=0.3)
ax5.legend()

ax6.plot(v_max, color='red', linewidth=2, label='Grip limit', alpha=0.5)
ax6.plot(v_final, color='black', linewidth=2, label='Final Velocity')
ax6.set_xlabel("Track Position (index)", fontsize=12)
ax6.set_ylabel("Velocity (m/s)", fontsize=12)
ax6.set_title('Velocity vs Position', fontsize=13)
ax6.grid(True, alpha=0.3)
ax6.legend()


plt.tight_layout()
plt.show()