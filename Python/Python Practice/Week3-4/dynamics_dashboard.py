# dynamics_dashboard.py

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

# DYNAMICS DASHBOARD — Analysis Notes
# 
# Did I ever exceed 1.5g combined?
# yes ast some point it was at -1.2 and -1.7
# Which direction had the highest acceleration?
# teh hgiegh accel was 1.7g of btakign and 1.2 of truning right 
# What was I doing when I recorded this data?
# not super sure 
# What would this plot look like if it were a real FSAE lap?
# hwop full teh plot woudl shwo closer to teh ouside edges mroe becoue teh driver would be opertgn closer to slip at te beging of fteh race 
#teh car woudl be at 0,0 and as it starte dacclign staritgh foward logitudal accel would go postive ten start turing left and acceling through teh corner teh point move to teh top right of teh circle 

# Car parameters
m = 300
g = 9.81
h = 0.3
trackwidth = 1.2
wheelbase = 1.6
g_limit = 1.5  # max lateral g

# Weight transfer functions
def lateral_weight_transfer(ay_g):
    return (m * ay_g * g * h) / trackwidth

def longitudinal_weight_transfer(ax_g):
    return (m * ax_g * g * h) / wheelbase

# Data ranges
a_range = np.linspace(0, 2.0, 100)
lat_transfer = lateral_weight_transfer(a_range)
long_transfer = longitudinal_weight_transfer(a_range)

# Friction circle
theta = np.linspace(0, 2 * np.pi, 300)
ax_circle = g_limit * np.cos(theta)
ay_circle = g_limit * np.sin(theta)

# Plot
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

# Lateral weight transfer
ax1.plot(a_range, lat_transfer, color='steelblue', linewidth=2.5)
ax1.axvline(x=1.5, color='gray', linestyle='--', alpha=0.6, label='1.5g limit')
ax1.set_xlabel('Lateral Acceleration (g)', fontsize=11)
ax1.set_ylabel('Weight Transfer (N)', fontsize=11)
ax1.set_title('Lateral Weight Transfer', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Longitudinal weight transfer
ax2.plot(a_range, long_transfer, color='firebrick', linewidth=2.5)
ax2.axvline(x=1.0, color='gray', linestyle='--', alpha=0.6, label='1.0g braking')
ax2.set_xlabel('Longitudinal Acceleration (g)', fontsize=11)
ax2.set_ylabel('Weight Transfer (N)', fontsize=11)
ax2.set_title('Longitudinal Weight Transfer', fontsize=12)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Friction circle
ax3.plot(ax_circle, ay_circle, color='darkgreen', linewidth=2.5)
ax3.axhline(0, color='black', linewidth=0.8, alpha=0.4)
ax3.axvline(0, color='black', linewidth=0.8, alpha=0.4)
ax3.set_xlabel('Longitudinal Acceleration (g)', fontsize=11)
ax3.set_ylabel('Lateral Acceleration (g)', fontsize=11)
ax3.set_title('Friction Circle — 1.5g limit', fontsize=12)
ax3.set_aspect('equal')
ax3.grid(True, alpha=0.3)
df = pd.read_csv('C:/Users/aiden/OneDrive/Documents/Summer Project/Python/Python Practice/accel.csv')
ax3.scatter(df['x_g'], df['y_g'], color='orange', s=20, alpha=0.6, label='Real data')
ax3.legend()

plt.tight_layout()
plt.savefig('dynamics_dashboard.png', dpi=150)
plt.show()