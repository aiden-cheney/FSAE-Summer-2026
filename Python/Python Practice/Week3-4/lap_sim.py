#=========================================================================
# lap_sim.py
# FSAE Lap Sim — Vehicle Dynamics Dashboard
# Aiden Cheney - 5/21/2026 (Weeks 3-4 (Founations))
#=========================================================================

import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 

#----------CAR PAREMTER-----------------------
m = 300             # kg, total mass
g = 9.81            # m/s², gravitational acceleration
h = 0.3             # m, CG height
trackwidth = 1.2    # m, lateral distance between contact patches
wheelbase = 1.6     # m, front to rear axle distance
g_limit    = 1.5    # max lateral g from friction circle
C_alpha    = 800    # N/deg, cornering stiffness
a_max = 10          # m/s², max acceleration
b_max = 15          # m/s², max braking acceleration
ds = 1      # m, approximate distance per track index step


#----------WEIGHT TRANSFER (FUNC 1)-----------------------

def weight_transfer(accel_range):
    """Given a range of accleration in g's it returns our lateral and longintudnal weight transfer"""

    lateral_weight_transfer = (m * accel_range * g * h) / trackwidth
    longitudinal_weight_transfer = (m * accel_range * g * h) / wheelbase

    return (lateral_weight_transfer, longitudinal_weight_transfer)

#----------FRICTION CIRCLE (FUNC 2)-----------------------

def friction_circle(g_limit):
    """Returns X/Y coordinates of the friction circle boundary and loads real accelerometer data for overlay."""  
    
    theta = np.linspace(0, 2 * np.pi, 300)

    accelx_circle = g_limit * np.cos(theta)
    accely_circle = g_limit * np.sin(theta)

    df = pd.read_csv(
    'C:/Users/aiden/OneDrive/Documents/Summer Project/'
    'Python/Python Practice/accel.csv'
    )
    
    return (accelx_circle, accely_circle, df)

#----------TIRE MODEL (FUNC 3)-----------------------

def tire_model (C_alpha):
    """ Linear tire model: lateral force = cornering stiffness xslip angle. Valid up to ~3 degrees. Returns slip angle array and force array."""

    alpha = np.linspace(0, 10, 200)  # degrees
    F_lateral = C_alpha * alpha

    return (alpha, F_lateral)

#---------- TRACK MAP (FUNC 4)-----------------------

def track():
    """Generates a synthetic FSAE-style oval track as X/Y coordinates and calculates curvature at every point."""

    t         = np.linspace(0, 2 * np.pi, 500)
    x         = 40 * np.cos(t) + 5 * np.cos(2 * t)
    y         = 20 * np.sin(t)
    dx        = np.diff(x)
    dy        = np.diff(y)
    ddx       = np.diff(dx)
    ddy       = np.diff(dy)
    curvature = (np.abs(dx[:-1] * ddy - dy[:-1] * ddx) / (dx[:-1]**2 + dy[:-1]**2)**1.5)
    
    return x, y, curvature

def final_velocity(curvature, g_limit, a_max, b_max, ds):
    """Calculates the final velocity of the vehicle given the max velocity and max braking acceleration."""
   
    v_max = np.sqrt(g_limit * 9.81 / curvature)
    v_forward = v_max.copy()  
    v_backward = v_max.copy() 

    for i in range(1, len(v_forward)):
        v_possiblefwd = np.sqrt(v_forward[i-1]**2 + 2 * a_max * ds)
        v_forward[i] = min(v_possiblefwd, v_max[i])

    for i in range(len(v_forward)-2, -1, -1):
        v_possiblebwd = np.sqrt(v_backward[i+1]**2 + 2 * b_max * ds)
        v_backward[i] = min(v_possiblebwd, v_max[i])

    v_final = np.minimum(v_forward, v_backward)

    return v_max, v_forward, v_backward, v_final


# ── MAIN ──────────────────────────────────────────────────────
if __name__ == "__main__":

    # Run all functions
    accel_range = np.linspace(0, 3, 300)
    lateral_weight_transfer, longitudinal_weight_transfer = weight_transfer(accel_range)
    ax_circle, ay_circle, df = friction_circle(g_limit)
    alpha, F_lateral = tire_model(C_alpha)
    x, y, curvature = track()
    v_max, v_forward, v_backward, v_final = final_velocity(curvature, g_limit, a_max, b_max, ds)

    # ── PLOT ──────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    ax1, ax2, ax3 = axes[0]
    ax4, ax5, ax6 = axes[1]

    # Weight transfer
    ax1.plot(accel_range, lateral_weight_transfer,  color='black', linewidth=2, label='Lateral')
    ax1.plot(accel_range, longitudinal_weight_transfer, color='red',  linewidth=2, label='Longitudinal')
    ax1.axvline(x=1.5, color='gray', linestyle='--', alpha=0.6, label='1.5g limit')
    ax1.set_xlabel('Acceleration (g)')
    ax1.set_ylabel('Weight Transfer (N)')
    ax1.set_title('Weight Transfer')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Friction circle with real data
    ax2.plot(ax_circle, ay_circle, color='black', linewidth=2)
    ax2.scatter(df['x_g'], df['y_g'], color='red', s=20, alpha=0.6, label='Real data')
    ax2.axhline(0, color='black', linewidth=0.8, alpha=0.4)
    ax2.axvline(0, color='black', linewidth=0.8, alpha=0.4)
    ax2.set_xlabel('Longitudinal Acceleration (g)')
    ax2.set_ylabel('Lateral Acceleration (g)')
    ax2.set_title(f'Friction Circle — {g_limit}g limit')
    ax2.set_aspect('equal')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Tire model (Slip angle)
    ax3.plot(alpha, F_lateral, color='black', linewidth=2, label='Linear model')
    ax3.axvline(x=3, color='red', linestyle='--', alpha=0.6, label='Linear limit (~3°)')
    ax3.set_xlabel('Slip Angle (degrees)', fontsize=12)
    ax3.set_ylabel('Lateral Force (N)', fontsize=12)
    ax3.set_title('Lateral Force vs Slip Angle — Linear Tire Model', fontsize=13)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Track map
    ax4.plot(x, y, color='black', linewidth=2)
    ax4.plot(x[0], y[0], 'go', color="red", markersize=8, label='Start/Finish')
    ax4.set_xlabel('X - Position (m)', fontsize=12)
    ax4.set_ylabel('Y - Position (m)', fontsize=12)
    ax4.set_title('FSAE Autocorss Track Layout', fontsize=13)
    ax4.legend()
    ax4.grid(True, alpha=0.3)


    # Curvature
    ax5.plot(curvature, color='black', linewidth=2)
    ax5.set_xlabel('Track Position (index)', fontsize=12)
    ax5.set_ylabel('Curvature (1/m)', fontsize=12)
    ax5.set_title('Track Curvature vs Position', fontsize=13)
    ax5.grid(True, alpha=0.3)

    # Final velocity
    ax6.plot(v_max, color='red', linewidth=2, label='Grip limit', alpha=0.5)
    ax6.plot(v_final, color='black', linewidth=2, label='Final Velocity')
    ax6.set_xlabel("Track Position (index)", fontsize=12)
    ax6.set_ylabel("Velocity (m/s)", fontsize=12)
    ax6.set_title('Velocity vs Position', fontsize=13)
    ax6.grid(True, alpha=0.3)
    ax6.legend()


    plt.tight_layout()
    plt.show()
