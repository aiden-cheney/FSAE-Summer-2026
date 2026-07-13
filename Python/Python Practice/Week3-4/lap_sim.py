#=========================================================================
# lap_sim.py
# FSAE Lap Sim — Vehicle Dynamics Dashboard (CANONICAL)
# Aiden Cheney
# History: Weeks 3-4 foundations -> Weeks 5-6 real Pacejka tire fit,
#          power/drag/downforce, 4-tire load-sensitive grip solver.
# Consolidated 2026-07-11: merges Week3-4/lap_sim.py (real GPS wiring,
#   6/30) with Week5-6/Untitled-1.py (real TTC tire fit + full physics
#   stack, 7/2). This is now the one canonical file — Untitled-1.py and
#   the old placeholder lap_sim.py are both superseded by this.
#=========================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

#----------PATHS-----------------------
UNIFIED_CSV = r'C:\Users\aiden\OneDrive\Documents\Summer Project\unified.csv'

#----------CAR PARAMETERS-----------------------
m          = 300     # kg, total mass
g          = 9.81    # m/s², gravitational acceleration
h          = 0.3     # m, CG height
trackwidth = 1.2     # m, lateral distance between contact patches
wheelbase  = 1.6     # m, front to rear axle distance
C_alpha    = 800      # N/deg, cornering stiffness (linear model, reference only)
a_max      = 10       # m/s², max acceleration
b_max      = 15       # m/s², max braking acceleration
power      = 60000    # W
rho        = 1.225    # kg/m³, air density
cd         = 1.5      # drag coefficient
area       = 1.0      # m², frontal area
cl         = 2.52     # downforce coefficient (team value, Orion Suspension Master)

# --- Tire model: Hoosier 16x7.5-10, Round 9 TTC fit @ 10psi, derated 0.75 ---
# (Resolved 2026-07-02 — supersedes the old placeholder guesses that were
#  still floating around in tire_model_pacejka.py: B=10.0, C=1.9, D=2800,
#  E=-1.5, which gave a fake single-tire-style 0.95g. Those numbers were
#  never a real per-tire/whole-car split disagreement — they were just an
#  early guess, superseded by a real TTC data fit once one existed.)
fx_max = 3710          # N, whole-car longitudinal peak (per-tire mu_x*Fz x4 x0.75)
B      = 20.85         # stiffness factor (from cornering stiffness Kya at Fz=736N)
C      = 1.411         # shape factor = PCY1
D      = 4180          # N, whole-car lateral peak (per-tire 1393 x4 x0.75) -> g_limit ~= 1.42g flat
E      = -1.027        # curvature = PEY1 + PEY2*dfz

# Tire load-sensitivity (for the 4-tire lateral limit) — same Hoosier fit
PDY1        = -1.90675844   # lateral friction mu_y at nominal load
PDY2        = 0.138253158   # variation of mu_y with load (dfz)
FNOMIN_TIRE = 670.57         # N, nominal wheel load for the fit
GRIP_SCALE  = 0.75            # lab-to-track grip derate


#----------WEIGHT TRANSFER-----------------------

def weight_transfer(accel_range):
    """Given a range of acceleration in g's, returns lateral and longitudinal weight transfer (N)."""
    lateral_weight_transfer      = (m * accel_range * g * h) / trackwidth
    longitudinal_weight_transfer = (m * accel_range * g * h) / wheelbase
    return (lateral_weight_transfer, longitudinal_weight_transfer)


#----------TIRE MODEL — PACEJKA (single-curve reference) -----------------------

def tire_model(C_alpha):
    """Linear tire model + Pacejka Magic Formula curve (flat single-D reference, not the
    grip-limit actually used — see peak_lateral_g() for the load-sensitive 4-tire version)."""
    alpha     = np.linspace(-15, 15, 500)
    alpha_rad = np.deg2rad(alpha)

    Fy = D * np.sin(C * np.arctan(B * alpha_rad - E * (B * alpha_rad - np.arctan(B * alpha_rad))))

    fy_linear = C_alpha * alpha
    fy_linear = np.clip(fy_linear, -D, D)

    F_lateral = C_alpha * alpha
    return (alpha, alpha_rad, F_lateral, fy_linear, Fy)


#---------- 4-TIRE LOAD-SENSITIVE GRIP LIMIT -----------------------

def peak_lateral_g(mass=m):
    """4-tire load-sensitive lateral limit.
    Lumped axle: left vs right pair, 2 tires each. Lateral load transfer
    dN = m*a*h/trackwidth shifts load to the outer pair; mu_y drops with load
    (PDY2), so transferring load loses total grip. Solved self-consistently
    (a = F_total/m). This is the real grip-limit input to the sim — the flat
    single-D Pacejka curve above is a reference/plotting curve, not this.
    """
    def mu(Fz):
        Fz = max(Fz, 1.0)
        return abs(PDY1 + PDY2 * ((Fz - FNOMIN_TIRE) / FNOMIN_TIRE))

    a = 1.4 * g
    for _ in range(60):
        dN    = mass * a * h / trackwidth
        Fz_out = mass * g / 2 + dN
        Fz_in  = max(mass * g / 2 - dN, 0.0)
        Fy = GRIP_SCALE * (2 * mu(Fz_out / 2) * (Fz_out / 2) +
                           2 * mu(Fz_in / 2) * (Fz_in / 2))
        a = Fy / mass
    return a / g


#----------FRICTION ELLIPSE-----------------------

def friction_circle(g_limit, peaklatforce):
    """Combined-slip friction ellipse boundary, plus real accelerometer data for overlay."""
    fx = np.linspace(0, fx_max, 500)
    fy_combined = peaklatforce * np.sqrt(1 - (fx / fx_max) ** 2)

    df = pd.read_csv(UNIFIED_CSV)
    df = df[pd.to_numeric(df['lat'], errors='coerce').notna()].copy()
    df['x_g'] = pd.to_numeric(df['x_g'], errors='coerce')
    df['y_g'] = pd.to_numeric(df['y_g'], errors='coerce')
    df = df.dropna(subset=['x_g', 'y_g'])
    return (df, fx, fy_combined)


#---------- SYNTHETIC TRACK -----------------------

def track():
    """Generates a synthetic FSAE-style oval track as X/Y coordinates, curvature, and real
    arc-length-derived distance-per-step (ds)."""
    t         = np.linspace(0, 2 * np.pi, 500)
    x         = 40 * np.cos(t) + 5 * np.cos(2 * t)
    y         = 20 * np.sin(t)
    dx        = np.diff(x)
    dy        = np.diff(y)
    ddx       = np.diff(dx)
    ddy       = np.diff(dy)
    track_length = np.sum(np.sqrt(dx ** 2 + dy ** 2))
    curvature = np.abs(dx[:-1] * ddy - dy[:-1] * ddx) / (dx[:-1] ** 2 + dy[:-1] ** 2) ** 1.5
    ds = track_length / len(dx)
    return x, y, curvature, track_length, ds


#---------- GPS TRACK FROM REAL DATA -----------------------

def gps_track(csv_path=None):
    """
    Reads unified.csv, projects lat/lng -> X/Y in meters (flat-earth approximation),
    and derives speed only between fixes where position actually changed (avoids
    false spikes from duplicate GPS fixes at the same position).

    Note: ~22 unique GPS fixes over ~5 minutes — a slow test ride, not a full
    autocross lap. Real, but not a like-for-like comparison to the sim lap time
    below (different event entirely) — see main() print notes.

    Also returns g_total per GPS row, computed directly from the accelerometer
    (not GPS-derived) — this is real, trustworthy data unlike the jitter-affected
    speed series, and is what colors the GPS path in the hero dashboard panel.
    """
    if csv_path is None:
        csv_path = UNIFIED_CSV
    df = pd.read_csv(csv_path)
    df = df[pd.to_numeric(df['lat'], errors='coerce').notna()].copy()
    for col in ['lat', 'lng', 'time', 'x_g', 'y_g']:
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
    # g_total from the same accelerometer rows as the GPS fix (real, direct sensor data —
    # unlike GPS-derived speed, not affected by GPS fix-jitter, so this is trustworthy
    # for the hero figure's g-force trace).
    g_total = np.sqrt(df['x_g'].fillna(0) ** 2 + df['y_g'].fillna(0) ** 2).values

    # Speed: only between rows where position actually changed
    pos_changed = (df['lat'].diff().abs() + df['lng'].diff().abs()) > 0
    df_unique = df[pos_changed].copy()
    x_u = (df_unique['lng'] - lng_ref) * MPD_lng
    y_u = (df_unique['lat'] - lat_ref) * MPD_lat
    t_u = df_unique['time'] / 1000.0

    dx = np.diff(x_u.values)
    dy = np.diff(y_u.values)
    dt = np.diff(t_u.values)
    # Guard against duplicate-row artifacts near power-cycle restarts: the logger's
    # real interval is ~0.5s, so any dt well below that (e.g. two rows straddling a
    # restart with near-zero real time between them) produces a fake huge speed spike.
    # Found during 2026-07-11 consolidation: one such row pair gave a false 1780 m/s.
    MIN_DT = 0.1  # s — below the logger's real ~0.5s cadence, treat as an artifact
    dt = np.where((dt == 0) | (dt < MIN_DT), np.nan, dt)
    speed_mps = np.sqrt(dx ** 2 + dy ** 2) / dt
    t_speed = (t_u.values[:-1] + t_u.values[1:]) / 2

    return x_m.values, y_m.values, t_s.values, t_speed, speed_mps, g_total


#---------- VELOCITY PROFILE (power + drag + downforce) -----------------------

def final_velocity(curvature, g_limit, a_max, b_max, ds, mass=m, cl_val=cl):
    """Forward/backward velocity integration: grip-limited cornering speed, adjusted for
    downforce, then capped by power-limited acceleration and drag going forward, and by
    braking capacity going backward."""
    v_max = np.sqrt(g_limit * 9.81 / np.maximum(curvature, 1e-6))
    F_downforce = 0.5 * rho * v_max ** 2 * cl_val * area
    g_limit_effective = g_limit + (F_downforce / (mass * 9.81))
    v_max_effective = np.sqrt(g_limit_effective * 9.81 / np.maximum(curvature, 1e-6))

    v_forward = v_max_effective.copy()
    v_backward = v_max_effective.copy()

    for i in range(1, len(v_forward)):
        a_power = power / (mass * v_forward[i - 1])
        a_dragfwd = (0.5 * rho * v_forward[i - 1] ** 2 * cd * area) / mass
        a_actualfwd = min(a_power, a_max) - a_dragfwd
        v_possiblefwd = np.sqrt(v_forward[i - 1] ** 2 + 2 * a_actualfwd * ds)
        v_forward[i] = min(v_possiblefwd, v_max_effective[i])

    for i in range(len(v_forward) - 2, -1, -1):
        a_dragbwd = (0.5 * rho * v_backward[i + 1] ** 2 * cd * area) / mass
        a_actualbwd = b_max + a_dragbwd
        v_possiblebwd = np.sqrt(v_backward[i + 1] ** 2 + 2 * a_actualbwd * ds)
        v_backward[i] = min(v_possiblebwd, v_max_effective[i])

    v_final = np.minimum(v_forward, v_backward)
    return v_max, v_max_effective, v_forward, v_backward, v_final


def lap_time(ds, v_final):
    """Sums time to traverse each segment given final velocity at each point."""
    dt = ds / v_final
    return np.sum(dt)


# ── MAIN ──────────────────────────────────────────────────────
if __name__ == "__main__":

    accel_range = np.linspace(0, 3, 300)
    lateral_wt, longitudinal_wt = weight_transfer(accel_range)

    alpha, alpha_rad, F_lateral, fy_linear, Fy = tire_model(C_alpha)

    g_limit = peak_lateral_g()
    peaklatforce = g_limit * m * g
    print(f"g_limit (4-tire, load-sensitive): {g_limit:.3f} g")

    df_accel, fx, fy_combined = friction_circle(g_limit, peaklatforce)
    print(f"Accel rows loaded: {len(df_accel)}")

    x, y, curvature, track_length, ds = track()
    v_max, v_max_eff, v_forward, v_backward, v_final = final_velocity(curvature, g_limit, a_max, b_max, ds)
    total_lap_time = lap_time(ds, v_final)
    print(f"Track length: {track_length:.2f} m, ds: {ds:.3f} m/step")
    print(f"Estimated lap time: {total_lap_time:.2f} s")

    # Mass sensitivity (grip is mass-independent here; only power-limited zones feel it)
    masses = np.arange(200, 450, 25)
    lap_times_mass = []
    for mass_test in masses:
        _, _, _, _, v_final_test = final_velocity(curvature, g_limit, a_max, b_max, ds, mass=mass_test)
        lap_times_mass.append(lap_time(ds, v_final_test))
    print("Mass sensitivity:", dict(zip(masses.tolist(), [round(t, 2) for t in lap_times_mass])))

    # CL (downforce) sensitivity — synthetic track only; real GPS track is too sparse
    # (slow test ride, not a competitive lap) for a meaningful curvature-based sensitivity study.
    cl_values = np.arange(1.0, 3.5, 0.25)
    lap_times_cl = []
    for cl_test in cl_values:
        _, _, _, _, v_final_test = final_velocity(curvature, g_limit, a_max, b_max, ds, cl_val=cl_test)
        lap_times_cl.append(lap_time(ds, v_final_test))
    print("CL sensitivity:", dict(zip([round(c, 2) for c in cl_values.tolist()], [round(t, 2) for t in lap_times_cl])))

    # Real GPS track + derived speed (overlay/comparison, not a curvature source for the sim —
    # see note in gps_track())
    x_gps, y_gps, t_gps, t_speed, speed_gps, g_total_gps = gps_track()
    n_unique = len(set(zip(x_gps.round(5), y_gps.round(5))))
    print(f"GPS rows loaded: {len(x_gps)} ({n_unique} unique positions)")
    print(f"GPS duration: {t_gps[-1] - t_gps[0]:.1f} s")
    print("NOTE: real GPS data is a slow bike test ride (~5 min, only ~21 unique resolved")
    print("      positions), not a competitive FSAE lap. Found 2026-07-11: the derived speed")
    print("      series is dominated by GPS fix-jitter -- with only ~21 distinct positions")
    print("      over 5 minutes, the module is mostly bouncing between a few nearby resolved")
    print("      fixes rather than tracking continuous motion, so consecutive-fix speed is")
    print("      not a trustworthy velocity signal yet (do not quote a 'max GPS speed'")
    print("      number anywhere recruiting-facing). Needs a denser real GPS log (a proper")
    print("      fix rate, ideally 1-5 Hz continuous lock) before this is usable data.")

    # ── PLOTS ──────────────────────────────────────────────────
    fig, axes = plt.subplots(3, 3, figsize=(16, 11))
    ax1, ax2, ax3 = axes[0]
    ax4, ax5, ax6 = axes[1]
    ax7, ax8, ax9 = axes[2]

    ax1.plot(accel_range, lateral_wt, color='black', linewidth=2, label='Lateral')
    ax1.plot(accel_range, longitudinal_wt, color='red', linewidth=2, label='Longitudinal')
    ax1.axvline(x=g_limit, color='gray', linestyle='--', alpha=0.6, label=f'{g_limit:.2f}g limit')
    ax1.set_xlabel('Acceleration (g)'); ax1.set_ylabel('Weight Transfer (N)')
    ax1.set_title('Weight Transfer'); ax1.legend(fontsize=8); ax1.grid(True, alpha=0.3)

    ax2.plot(fx / (m * g), fy_combined / (m * g), color='black', linewidth=2)
    ax2.plot(-fx / (m * g), fy_combined / (m * g), color='black', linewidth=2)
    ax2.plot(fx / (m * g), -fy_combined / (m * g), color='black', linewidth=2)
    ax2.plot(-fx / (m * g), -fy_combined / (m * g), color='black', linewidth=2)
    ax2.scatter(df_accel['x_g'], df_accel['y_g'], color='red', s=10, alpha=0.6, label='Real accel data')
    ax2.axhline(0, color='black', linewidth=0.8, alpha=0.4); ax2.axvline(0, color='black', linewidth=0.8, alpha=0.4)
    ax2.set_xlabel('Longitudinal Accel (g)'); ax2.set_ylabel('Lateral Accel (g)')
    ax2.set_title(f'Friction Ellipse — {g_limit:.2f}g limit'); ax2.set_aspect('equal')
    ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)

    ax3.plot(alpha, F_lateral, color='black', linewidth=2, label='Linear model')
    ax3.plot(alpha, fy_linear, color='blue', linewidth=2, label='Clipped linear')
    ax3.plot(alpha, Fy, color='red', linewidth=2, label='Pacejka (flat-D reference)')
    ax3.axvline(x=3, color='red', linestyle='--', alpha=0.6, label='Linear limit (~3°)')
    ax3.set_xlabel('Slip Angle (deg)'); ax3.set_ylabel('Lateral Force (N)')
    ax3.set_title('Lateral Force vs Slip Angle'); ax3.legend(fontsize=8); ax3.grid(True, alpha=0.3)

    ax4.plot(x, y, color='black', linewidth=2)
    ax4.plot(x[0], y[0], 'o', color='red', markersize=8, label='Start/Finish')
    ax4.set_xlabel('X (m)'); ax4.set_ylabel('Y (m)')
    ax4.set_title('Synthetic FSAE Track')
    ax4.text(0.5, 0.55, f'Lap: {total_lap_time:.2f}s', fontsize=9, ha='center', transform=ax4.transAxes)
    ax4.text(0.5, 0.45, f'Length: {track_length:.1f}m', fontsize=9, ha='center', transform=ax4.transAxes)
    ax4.legend(fontsize=8); ax4.grid(True, alpha=0.3)

    ax5.plot(curvature, color='black', linewidth=2)
    ax5.set_xlabel('Track Position (index)'); ax5.set_ylabel('Curvature (1/m)')
    ax5.set_title('Track Curvature vs Position'); ax5.grid(True, alpha=0.3)

    ax6.plot(v_max_eff, color='red', linewidth=2, alpha=0.5, label='Grip limit')
    ax6.plot(v_final, color='black', linewidth=2, label='Final Velocity')
    ax6.set_xlabel('Track Position (index)'); ax6.set_ylabel('Velocity (m/s)')
    ax6.set_title('Velocity vs Position (synthetic track)')
    ax6.grid(True, alpha=0.3); ax6.legend(fontsize=8)

    ax7.plot(masses, lap_times_mass, color='black', linewidth=2, marker='o', label='vs Mass')
    ax7.set_xlabel('Mass (kg)'); ax7.set_ylabel('Lap Time (s)')
    ax7.set_title('Lap Time Sensitivity — Mass'); ax7.grid(True, alpha=0.3)

    ax8.plot(cl_values, lap_times_cl, color='darkgreen', linewidth=2, marker='o')
    ax8.axvline(x=cl, color='gray', linestyle='--', alpha=0.6, label=f'Team CL={cl}')
    ax8.set_xlabel('Downforce Coefficient (CL)'); ax8.set_ylabel('Lap Time (s)')
    ax8.set_title('Lap Time Sensitivity — CL'); ax8.legend(fontsize=8); ax8.grid(True, alpha=0.3)

    # GPS path colored by g-force: position from GPS (real, if sparse), color from the
    # accelerometer (real, direct sensor data — not affected by GPS fix-jitter, unlike a
    # GPS-derived speed trace would be). This is the "real-world overlay" hero panel.
    sc = ax9.scatter(x_gps, y_gps, c=g_total_gps, cmap='hot', s=25, edgecolors='none')
    ax9.plot(x_gps, y_gps, color='gray', linewidth=0.5, alpha=0.4, zorder=0)
    ax9.set_xlabel('X (m)'); ax9.set_ylabel('Y (m)')
    ax9.set_title(f'Real GPS Path, colored by g-force\n({n_unique} unique fixes, ~5 min bike test ride)')
    ax9.set_aspect('equal'); ax9.grid(True, alpha=0.3)
    plt.colorbar(sc, ax=ax9, label='g_total', fraction=0.046, pad=0.04)

    plt.suptitle('FSAE Lap Sim Dashboard — Canonical (Pacejka, 4-tire grip, power/drag/downforce)',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('lap_sim_dashboard.png', dpi=150)

    # ── SYNTHETIC VALIDATION RIDE (separate figure, clearly labeled) ─────────────
    # synthetic_ride.csv is NOT real logged data — it's a physically-modeled synthetic ride
    # (generate_synthetic_ride.py), used to validate the same GPS/accelerometer pipeline with
    # denser, cleaner data while real field data collection is paused. Kept in its own figure,
    # never merged into the real-data hero dashboard above.
    import os
    synth_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'synthetic_ride.csv')
    if os.path.exists(synth_path):
        xs_syn, ys_syn, ts_syn, tspeed_syn, speed_syn, g_syn = gps_track(csv_path=synth_path)
        n_unique_syn = len(set(zip(xs_syn.round(5), ys_syn.round(5))))

        fig2, (bx1, bx2) = plt.subplots(1, 2, figsize=(13, 6))

        sc2 = bx1.scatter(xs_syn, ys_syn, c=g_syn, cmap='hot', s=12, edgecolors='none')
        bx1.plot(xs_syn, ys_syn, color='gray', linewidth=0.5, alpha=0.4, zorder=0)
        bx1.set_xlabel('X (m)'); bx1.set_ylabel('Y (m)')
        bx1.set_title(f'Synthetic Validation Ride — GPS Path by g-force\n({n_unique_syn} points, 3 laps around a modeled city block)')
        bx1.set_aspect('equal'); bx1.grid(True, alpha=0.3)
        plt.colorbar(sc2, ax=bx1, label='g_total', fraction=0.046, pad=0.04)

        valid_syn = ~np.isnan(speed_syn)
        bx2.plot(tspeed_syn[valid_syn], speed_syn[valid_syn], color='steelblue', linewidth=1.5)
        bx2.set_xlabel('Time (s)'); bx2.set_ylabel('Speed (m/s)')
        bx2.set_title('Synthetic Validation Ride — Speed vs Time\n(dense/clean by construction, not fix-jitter limited like the real log)')
        bx2.grid(True, alpha=0.3)

        fig2.suptitle('SYNTHETIC VALIDATION DATASET (simulated, not logged) — see generate_synthetic_ride.py',
                      fontsize=12, fontweight='bold', color='darkred')
        plt.tight_layout()
        plt.savefig('synthetic_ride_dashboard.png', dpi=150)
        print(f"Synthetic validation ride: {len(xs_syn)} rows, {n_unique_syn} unique points, "
              f"saved synthetic_ride_dashboard.png")

    plt.show()
