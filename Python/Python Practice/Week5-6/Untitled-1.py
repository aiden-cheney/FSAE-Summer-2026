# NOTE (2026-07-11): superseded. This file's physics (Pacejka TTC fit, 4-tire
# load-sensitive grip, power/drag/downforce) has been consolidated into the
# canonical Week3-4/lap_sim.py. Kept here for history only -- don't edit further.
# Aiden Cheney - 5/23/2026 (Lap time v1)
# Updated: 2026-06-30 — fixed unified.csv path, GPS speed panel, curvature clamp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

#----------CAR PAREMTER-----------------------
m = 300             # kg, total mass
g = 9.81            # m/s², gravitational acceleration
h = 0.3             # m, CG height
trackwidth = 1.2    # m, lateral distance between contact patches
wheelbase  = 1.6    # m, front to rear axle distance
g_limit    = 1.5    # max lateral g from friction circle
C_alpha    = 800    # N/deg, cornering stiffness
a_max = 10          # m/s², max acceleration
power = 60000
b_max = 15          # m/s², max braking acceleration
rho = 1.225         # kg/m³, air density
cd = 1.5            # drag coefficient
area = 1.0          # m², frontal area
cl = 2.52           # downforce coefficient
# --- Tire model: Hoosier 16x7.5-10, Round 9 TTC fit @ 10psi, derated 0.75 (updated 2026-07-02) ---
# Old placeholder guesses: fx_max=3200, B=10.0, C=1.9, D=2800, E=-1.5  (D gave a fake 0.95g)
fx_max = 3710         # N, whole-car longitudinal peak (per-tire mu_x*Fz x4 x0.75)
B = 20.85             # stiffness factor (from cornering stiffness Kya at Fz=736N)
C = 1.411             # shape factor = PCY1
D = 4180              # N, whole-car lateral peak (per-tire 1393 x4 x0.75) -> g_limit ~= 1.42g
E = -1.027            # curvature = PEY1 + PEY2*dfz

# Tire load-sensitivity (for 4-tire lateral limit) — Hoosier 16x7.5-10 @ 10psi
PDY1 = -1.90675844    # lateral friction mu_y at nominal load
PDY2 = 0.138253158    # variation of mu_y with load (dfz)
FNOMIN_TIRE = 670.57  # N, nominal wheel load for the fit
GRIP_SCALE = 0.75     # lab-to-track grip derate

#----------WEIGHT TRANSFER (FUNC 1)-----------------------

def weight_transfer(accel_range):
    """Given a range of accleration in g's it returns our lateral and longintudnal weight transfer"""
    lateral_weight_transfer = (m * accel_range * g * h) / trackwidth
    longitudinal_weight_transfer = (m * accel_range * g * h) / wheelbase
    return (lateral_weight_transfer, longitudinal_weight_transfer)

#----------FRICTION CIRCLE (FUNC 2)-----------------------

def friction_circle(g_limit, peaklatforce):
    """Returns X/Y coordinates of the friction circle boundary and loads real accelerometer data for overlay."""  

    fx = np.linspace(0, fx_max, 500)  # N, range of longitudinal forces for tire model
    fy_combined = peaklatforce * np.sqrt(1 - (fx / fx_max)**2)  # N, combined slip lateral force limit based on friction circle

    df = pd.read_csv('C:/Users/aiden/OneDrive/Documents/Summer Project/unified.csv')
    df = df[pd.to_numeric(df['lat'], errors='coerce').notna()].copy()
    df['x_g'] = pd.to_numeric(df['x_g'], errors='coerce')
    df['y_g'] = pd.to_numeric(df['y_g'], errors='coerce')
    df = df.dropna(subset=['x_g', 'y_g'])
    return (df, fx, fy_combined)

#----------TIRE MODEL (FUNC 3)-----------------------

def tire_model(C_alpha):
    """ Linear tire model: lateral force = cornering stiffness x slip angle. Valid up to ~3 degrees."""
    alpha = np.linspace(-15, 15, 500)
    alpha_rad = np.deg2rad(alpha)


    Fy = D * np.sin(C * np.arctan(B * alpha_rad - E * (B * alpha_rad - np.arctan(B * alpha_rad))))  
    
        
    fy_linear = 800 * alpha
    fy_linear = np.clip(fy_linear, -2800, 2800)

    F_lateral = C_alpha * alpha
    peaklatforce = np.max(Fy)
    
    g_limit = peaklatforce / (m * g)
    
    return (alpha, alpha_rad, F_lateral, fy_linear, Fy, g_limit, peaklatforce)

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
    track_length = np.sum(np.sqrt(dx**2 + dy**2))
    curvature = (np.abs(dx[:-1] * ddy - dy[:-1] * ddx) / (dx[:-1]**2 + dy[:-1]**2)**1.5)
    distance_sec = track_length / len(dx)
    return x, y, curvature, track_length, distance_sec

def final_velocity(curvature, g_limit, a_max, b_max, ds):
    """Calculates the final velocity of the vehicle given the max velocity and max braking acceleration."""
    v_max = np.sqrt(g_limit * 9.81 / np.maximum(curvature, 1e-6))  # clamp avoids div-by-zero on straights
    F_downforce = 0.5 * rho * v_max**2 * cl * area
    g_limit_effective = g_limit + (F_downforce / (m * 9.81))
    v_max_effective = np.sqrt(g_limit_effective * 9.81 / curvature)

    v_forward = v_max_effective.copy()  
    v_backward = v_max_effective.copy() 

    for i in range(1, len(v_forward)):
        a_power = power / (m * v_forward[i-1])
        a_dragfwd = (0.5 * rho * v_forward[i-1]**2 * cd * area) / m
        a_actualfwd = min(a_power, a_max) - a_dragfwd
        v_possiblefwd = np.sqrt(v_forward[i-1]**2 + 2 * a_actualfwd * ds)
        v_forward[i] = min(v_possiblefwd, v_max_effective[i])

    for i in range(len(v_forward)-2, -1, -1):
        a_dragbwd = (0.5 * rho * v_backward[i+1]**2 * cd * area) / m
        a_actualbwd = b_max + a_dragbwd
        v_possiblebwd = np.sqrt(v_backward[i+1]**2 + 2 * a_actualbwd * ds)
        v_backward[i] = min(v_possiblebwd, v_max_effective[i]) 

    v_final = np.minimum(v_forward, v_backward)
    return v_max, v_max_effective, v_forward, v_backward, v_final

def gps_track():
    """
    Reads unified.csv, projects lat/lng → X/Y in meters (flat-earth),
    and derives speed from consecutive GPS fixes.
    ~22 unique positions over 5 min — slow test run, not a full autocross lap.
    Returns: x_m, y_m, t_s, t_speed, speed_mps
    """
    df = pd.read_csv('C:/Users/aiden/OneDrive/Documents/Summer Project/unified.csv')
    df = df[pd.to_numeric(df['lat'], errors='coerce').notna()].copy()
    for col in ['lat', 'lng', 'time']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['lat', 'lng', 'time'])
    df = df[(df['lat'] != 0) & (df['lng'] != 0)]
    df = df.sort_values('time').reset_index(drop=True)

    lat_ref = df['lat'].iloc[0]
    lng_ref = df['lng'].iloc[0]
    MPD_lat = 111320
    MPD_lng = 111320 * math.cos(math.radians(lat_ref))

    x_m = (df['lng'] - lng_ref) * MPD_lng
    y_m = (df['lat'] - lat_ref) * MPD_lat
    t_s = df['time'] / 1000.0

    # Speed: only compute between rows where position actually changed
    # (duplicate GPS fixes cause huge false spikes if included)
    pos_changed = (df['lat'].diff().abs() + df['lng'].diff().abs()) > 0
    df_unique = df[pos_changed].copy()
    x_u = (df_unique['lng'] - lng_ref) * MPD_lng
    y_u = (df_unique['lat'] - lat_ref) * MPD_lat
    t_u = df_unique['time'] / 1000.0

    dx = np.diff(x_u.values)
    dy = np.diff(y_u.values)
    dt = np.diff(t_u.values)
    dt = np.where(dt == 0, np.nan, dt)
    speed_mps = np.sqrt(dx**2 + dy**2) / dt
    t_speed = (t_u.values[:-1] + t_u.values[1:]) / 2

    return x_m.values, y_m.values, t_s.values, t_speed, speed_mps


def lap_time(ds, v_final):
    """Calculates lap time by summing the time to traverse each segment of the track based on final velocity."""
    dt = ds / v_final
    total_time = np.sum(dt)
    return total_time


def peak_lateral_g():
    """4-tire load-sensitive lateral limit (added 2026-07-02).
    Lumped axle: left vs right pair, 2 tires each. Lateral load transfer
    dN = m*a*h/trackwidth shifts load to the outer pair; mu_y drops with load
    (PDY2), so transferring load loses total grip. Solved self-consistently
    (a = F_total/m). Returns g_limit accounting for that loss.
    """
    def mu(Fz):
        Fz = max(Fz, 1.0)
        return abs(PDY1 + PDY2 * ((Fz - FNOMIN_TIRE) / FNOMIN_TIRE))
    a = 1.4 * g
    for _ in range(60):
        dN = m * a * h / trackwidth
        Fz_out = m * g / 2 + dN
        Fz_in = max(m * g / 2 - dN, 0.0)
        Fy = GRIP_SCALE * (2 * mu(Fz_out / 2) * (Fz_out / 2) +
                           2 * mu(Fz_in / 2) * (Fz_in / 2))
        a = Fy / m
    return a / g


# ── MAIN ──────────────────────────────────────────────────────
if __name__ == "__main__":

    accel_range = np.linspace(0, 3, 300)
    lateral_weight_transfer, longitudinal_weight_transfer = weight_transfer(accel_range)
    alpha, alpha_rad, F_lateral, fy_linear, Fy, g_limit, peaklatforce = tire_model(C_alpha)
    # Override the flat single-curve limit with the 4-tire load-sensitive one
    g_limit = peak_lateral_g()
    peaklatforce = g_limit * m * g   # keep friction ellipse consistent with the limit
    print(f"g_limit (4-tire, load-sensitive): {g_limit:.3f} g")
    df, fx, fy_combined = friction_circle(g_limit, peaklatforce)
    print(f"Rows loaded: {len(df)}") 
    print(df.tail(3))
    x, y, curvature, track_length, distance_sec = track()
    v_max, v_max_effective, v_forward, v_backward, v_final = final_velocity(curvature, g_limit, a_max, b_max, distance_sec)
    total_lap_time = lap_time(distance_sec, v_final)
    print(f"Estimated lap time: {total_lap_time:.2f} seconds")
    print(f"v_corner: {np.sqrt(g_limit * 9.81 / 0.15):.2f} m/s")

    # GPS track + derived speed
    x_gps, y_gps, t_gps, t_speed, speed_gps = gps_track()

    # load unified GPS + accel data (for G-force map)
    gps_df = pd.read_csv('C:/Users/aiden/OneDrive/Documents/Summer Project/unified.csv')
    gps_df = gps_df[gps_df['lat'] != 'lat']
    gps_df = gps_df.apply(pd.to_numeric, errors='coerce')
    gps_df = gps_df[gps_df['lat'] != 0].dropna()
    gps_df['g_total'] = np.sqrt(gps_df['x_g']**2 + gps_df['y_g']**2)

    masses = np.arange(200, 450, 25)
    lap_times = []
    for m in masses:
        v_max_test, v_max_effective_test, v_forward_test, v_backward_test, v_final_test = final_velocity(curvature, g_limit, a_max, b_max, distance_sec)
        total_lap_time_test = lap_time(distance_sec, v_final_test)
        print(f"Mass: {m} kg - Estimated Lap Time: {total_lap_time_test:.2f} seconds")
        lap_times.append(total_lap_time_test)
    m = 300

    # ── PLOT ──────────────────────────────────────────────────
    fig, axes = plt.subplots(3, 3, figsize=(15, 10))
    ax1, ax2, ax3 = axes[0]
    ax4, ax5, ax6 = axes[1]
    ax7, ax8, ax9 = axes[2]

    ax1.plot(accel_range, lateral_weight_transfer, color='black', linewidth=2, label='Lateral')
    ax1.plot(accel_range, longitudinal_weight_transfer, color='red', linewidth=2, label='Longitudinal')
    ax1.axvline(x=1.5, color='gray', linestyle='--', alpha=0.6, label='1.5g limit')
    ax1.set_xlabel('Acceleration (g)')
    ax1.set_ylabel('Weight Transfer (N)')
    ax1.set_title('Weight Transfer')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    ax2.plot(fx / (m * g),  fy_combined / (m * g), color='black', linewidth=2)
    ax2.plot(-fx / (m * g), fy_combined / (m * g), color='black', linewidth=2)
    ax2.plot(fx / (m * g), -fy_combined / (m * g), color='black', linewidth=2)
    ax2.plot(-fx / (m * g),-fy_combined / (m * g), color='black', linewidth=2)
    ax2.scatter(df['x_g'], df['y_g'], color='red', s=10, alpha=0.6, label='Real data')
    ax2.axhline(0, color='black', linewidth=0.8, alpha=0.4)
    ax2.axvline(0, color='black', linewidth=0.8, alpha=0.4)
    ax2.set_xlabel('Longitudinal Acceleration (g)')
    ax2.set_ylabel('Lateral Acceleration (g)')
    ax2.set_title(f'Friction ellipse — {g_limit:.2f}g limit')
    ax2.set_aspect('equal')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    ax3.plot(alpha, F_lateral, color='black', linewidth=2, label='Linear model')
    ax3.plot(alpha, fy_linear, color='blue', linewidth=2, label='Clipped linear')
    ax3.plot(alpha, Fy, color='red', linewidth=2, label='Pacejka model')
    ax3.axvline(x=3, color='red', linestyle='--', alpha=0.6, label='Linear limit (~3°)')
    ax3.set_xlabel('Slip Angle (degrees)')
    ax3.set_ylabel('Lateral Force (N)')
    ax3.set_title('Lateral Force vs Slip Angle')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)

    ax4.plot(x, y, color='black', linewidth=2)
    ax4.plot(x[0], y[0], 'o', color="red", markersize=8, label='Start/Finish')
    ax4.set_xlabel('X - Position (m)')
    ax4.set_ylabel('Y - Position (m)')
    ax4.set_title('FSAE Autocross Track Layout')
    ax4.text(0.5, 0.55, f'Lap: {total_lap_time:.2f}s', fontsize=9, ha='center', transform=ax4.transAxes)
    ax4.text(0.5, 0.45, f'Length: {track_length:.1f}m', fontsize=9, ha='center', transform=ax4.transAxes)
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)

    ax5.plot(curvature, color='black', linewidth=2)
    ax5.set_xlabel('Track Position (index)')
    ax5.set_ylabel('Curvature (1/m)')
    ax5.set_title('Track Curvature vs Position')
    ax5.grid(True, alpha=0.3)

    ax6.plot(v_max_effective, color='red', linewidth=2, label='Grip limit', alpha=0.5)
    ax6.plot(v_final, color='black', linewidth=2, label='Final Velocity')
    ax6.set_xlabel("Track Position (index)")
    ax6.set_ylabel("Velocity (m/s)")
    ax6.set_title('Velocity vs Position')
    ax6.grid(True, alpha=0.3)
    ax6.legend(fontsize=8)

    ax7.plot(masses, lap_times, color='black', linewidth=2)
    ax7.set_xlabel("Mass (kg)")
    ax7.set_ylabel("Lap Time (s)")
    ax7.set_title('Lap Time vs Mass')
    ax7.grid(True, alpha=0.3)

    sc = ax8.scatter(gps_df['lng'], gps_df['lat'], c=gps_df['g_total'], cmap='hot', s=15)
    plt.colorbar(sc, ax=ax8, label='G-force magnitude')
    ax8.set_xlabel("Longitude")
    ax8.set_ylabel("Latitude")
    ax8.set_title('GPS Path — Color by G-force')
    ax8.grid(True, alpha=0.3)

    # GPS-derived speed vs time (real data)
    valid = ~np.isnan(speed_gps)
    ax9.plot(t_speed[valid], speed_gps[valid], color='steelblue', linewidth=2, label='GPS speed (real)')
    ax9.axhline(np.nanmean(speed_gps), color='gray', linestyle='--', alpha=0.7, label=f'Mean: {np.nanmean(speed_gps):.2f} m/s')
    ax9.set_xlabel('Time (s)')
    ax9.set_ylabel('Speed (m/s)')
    ax9.set_title('Real GPS Speed vs Time\n(sparse fixes — slow test run)')
    ax9.legend(fontsize=8)
    ax9.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()