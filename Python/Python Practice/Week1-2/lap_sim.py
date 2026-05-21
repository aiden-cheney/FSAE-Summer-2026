# =============================================================
# lap_sim.py
# FSAE Lap Time Simulator — Aiden Cheney, Summer 2026
# Weeks 3-4: Vehicle Dynamics Foundation
# =============================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ── CAR PARAMETERS ───────────────────────────────────────────
# Change these to match your actual car later
m          = 300    # kg, total mass
g          = 9.81   # m/s²
h          = 0.3    # m, CG height
trackwidth = 1.2    # m, lateral distance between contact patches
wheelbase  = 1.6    # m, front to rear axle distance
g_limit    = 1.5    # max lateral g from friction circle
C_alpha    = 800    # N/deg, cornering stiffness
a_max      = 10     # m/s², max acceleration
a_brake    = 15     # m/s², max braking
ds         = 1      # m, approximate distance per track index step


# ── FUNCTION 1: WEIGHT TRANSFER ───────────────────────────────
def calculate_weight_transfer(a_range):
    """
    Given a range of accelerations in g's, returns lateral
    and longitudinal weight transfer in Newtons.
    """
    lat  = (m * a_range * g * h) / trackwidth
    long = (m * a_range * g * h) / wheelbase
    return lat, long


# ── FUNCTION 2: FRICTION CIRCLE ───────────────────────────────
def build_friction_circle(g_limit):
    """
    Returns X/Y coordinates of the friction circle boundary
    and loads real accelerometer data for overlay.
    """
    theta     = np.linspace(0, 2 * np.pi, 300)
    ax_circle = g_limit * np.cos(theta)
    ay_circle = g_limit * np.sin(theta)

    df = pd.read_csv(
        'C:/Users/aiden/OneDrive/Documents/Summer Project/'
        'Python/Python Practice/accel.csv'
    )
    return ax_circle, ay_circle, df


# ── FUNCTION 3: TIRE MODEL ────────────────────────────────────
def build_tire_model(C_alpha):
    """
    Linear tire model: lateral force = cornering stiffness × slip angle.
    Valid up to ~3 degrees. Returns slip angle array and force array.
    """
    alpha    = np.linspace(0, 10, 200)   # degrees
    F_lateral = C_alpha * alpha
    return alpha, F_lateral


# ── FUNCTION 4: TRACK MAP ─────────────────────────────────────
def build_track():
    """
    Generates a synthetic FSAE-style oval track as X/Y coordinates
    and calculates curvature at every point.
    """
    t         = np.linspace(0, 2 * np.pi, 500)
    x         = 40 * np.cos(t) + 5 * np.cos(2 * t)
    y         = 20 * np.sin(t)
    dx        = np.diff(x)
    dy        = np.diff(y)
    ddx       = np.diff(dx)
    ddy       = np.diff(dy)
    curvature = (np.abs(dx[:-1] * ddy - dy[:-1] * ddx)
                 / (dx[:-1]**2 + dy[:-1]**2)**1.5)
    return x, y, curvature


# ── FUNCTION 5: SPEED PROFILE ─────────────────────────────────
def calculate_speed_profile(curvature, g_limit, a_max, a_brake, ds):
    """
    From curvature, calculates:
      v_max     — grip-limited corner speed at every point
      v_forward — forward pass (acceleration out of corners)
      v_backward— backward pass (braking into corners)
      v_final   — minimum of forward and backward = realistic speed
    """
    v_max      = np.sqrt(g_limit * 9.81 / curvature)

    v_forward  = v_max.copy()
    for i in range(1, len(v_forward)):
        v_possible    = np.sqrt(v_forward[i-1]**2 + 2 * a_max * ds)
        v_forward[i]  = min(v_possible, v_max[i])

    v_backward = v_max.copy()
    for i in range(len(v_backward)-2, -1, -1):
        v_possible     = np.sqrt(v_backward[i+1]**2 + 2 * a_brake * ds)
        v_backward[i]  = min(v_possible, v_max[i])

    v_final = np.minimum(v_forward, v_backward)
    return v_max, v_forward, v_backward, v_final


# ── MAIN ──────────────────────────────────────────────────────
if __name__ == "__main__":

    # Run all functions
    a_range                          = np.linspace(0, 2.0, 100)
    lat_transfer, long_transfer      = calculate_weight_transfer(a_range)
    ax_circle, ay_circle, df         = build_friction_circle(g_limit)
    alpha, F_lateral                 = build_tire_model(C_alpha)
    x, y, curvature                  = build_track()
    v_max, v_fwd, v_bwd, v_final     = calculate_speed_profile(curvature, g_limit, a_max, a_brake, ds)

    # ── PLOT ──────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    ax1, ax2, ax3 = axes[0]
    ax4, ax5, ax6 = axes[1]

    # Weight transfer
    ax1.plot(a_range, lat_transfer,  color='steelblue', linewidth=2, label='Lateral')
    ax1.plot(a_range, long_transfer, color='firebrick',  linewidth=2, label='Longitudinal')
    ax1.axvline(x=1.5, color='gray', linestyle='--', alpha=0.6, label='1.5g limit')
    ax1.set_xlabel('Acceleration (g)')
    ax1.set_ylabel('Weight Transfer (N)')
    ax1.set_title('Weight Transfer')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Friction circle with real data
    ax2.plot(ax_circle, ay_circle, color='darkgreen', linewidth=2.5)
    ax2.scatter(df['x_g'], df['y_g'], color='orange', s=20, alpha=0.6, label='Real data')
    ax2.axhline(0, color='black', linewidth=0.8, alpha=0.4)
    ax2.axvline(0, color='black', linewidth=0.8, alpha=0.4)
    ax2.set_xlabel('Longitudinal Acceleration (g)')
    ax2.set_ylabel('Lateral Acceleration (g)')
    ax2.set_title(f'Friction Circle — {g_limit}g limit')
    ax2.set_aspect('equal')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Tire model
    ax3.plot(alpha, F_lateral, color='darkorange', linewidth=2.5)
    ax3.axvline(x=3, color='gray', linestyle='--', alpha=0.6, label='Linear limit (~3°)')
    ax3.set_xlabel('Slip Angle (degrees)')
    ax3.set_ylabel('Lateral Force (N)')
    ax3.set_title('Linear Tire Model')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Track map
    ax4.plot(x, y, color='steelblue', linewidth=2.5)
    ax4.plot(x[0], y[0], 'go', markersize=10, label='Start/Finish')
    ax4.set_xlabel('X Position (m)')
    ax4.set_ylabel('Y Position (m)')
    ax4.set_title('Track Layout')
    ax4.axis('equal')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Curvature
    ax5.plot(curvature, color='purple', linewidth=2)
    ax5.set_xlabel('Track Position (index)')
    ax5.set_ylabel('Curvature (1/m)')
    ax5.set_title('Track Curvature')
    ax5.grid(True, alpha=0.3)

    # Speed profile
    ax6.plot(v_max,   color='red',   linewidth=2, alpha=0.5, label='Grip limit')
    ax6.plot(v_fwd,   color='blue',  linewidth=1.5, alpha=0.7, label='Forward pass')
    ax6.plot(v_bwd,   color='green', linewidth=1.5, alpha=0.7, label='Backward pass')
    ax6.plot(v_final, color='black', linewidth=2, label='Final speed')
    ax6.set_xlabel('Track Position (index)')
    ax6.set_ylabel('Velocity (m/s)')
    ax6.set_title('Speed Profile')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.suptitle('FSAE Lap Sim — Vehicle Dynamics Dashboard', fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig('lap_sim_dashboard.png', dpi=150)
    plt.show()