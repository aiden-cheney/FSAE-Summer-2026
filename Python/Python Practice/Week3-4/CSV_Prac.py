# weight_transfer.py

import numpy as np
import matplotlib.pyplot as plt

# Car parameters
m = 300       # kg, total mass
g = 9.81      # m/s²
h = 0.3       # m, center of gravity height
trackwidth = 1.2  # m, lateral distance between contact patches
wheelbase = 1.6   # m, front to rear axle distance

def lateral_weight_transfer(ay_g):
    ay = ay_g * g
    return (m * ay * h) / trackwidth

def longitudinal_weight_transfer(ax_g):
    ax = ax_g * g
    return (m * ax * h) / wheelbase

a_range = np.linspace(0, 2.0, 100)

lat_transfer = lateral_weight_transfer(a_range)
long_transfer = longitudinal_weight_transfer(a_range)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(a_range, lat_transfer, color='steelblue', linewidth=2.5)
ax1.set_xlabel('Lateral Acceleration (g)', fontsize=12)
ax1.set_ylabel('Weight Transfer (N)', fontsize=12)
ax1.set_title('Lateral Weight Transfer — 300 kg Car', fontsize=13)
ax1.axvline(x=1.5, color='gray', linestyle='--', alpha=0.6, label='1.5g limit')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(a_range, long_transfer, color='firebrick', linewidth=2.5)
ax2.set_xlabel('Longitudinal Acceleration (g)', fontsize=12)
ax2.set_ylabel('Weight Transfer (N)', fontsize=12)
ax2.set_title('Longitudinal Weight Transfer — 300 kg Car', fontsize=13)
ax2.axvline(x=1.0, color='gray', linestyle='--', alpha=0.6, label='1.0g braking')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('weight_transfer.png', dpi=150)
plt.show()

if __name__ == "__main__":
    print(f"At 1.5g lateral: {lateral_weight_transfer(1.5):.1f} N transferred")
    print(f"At 1.0g braking: {longitudinal_weight_transfer(1.0):.1f} N transferred")