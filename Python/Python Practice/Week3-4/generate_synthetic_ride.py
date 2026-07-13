#=========================================================================
# generate_synthetic_ride.py
# SYNTHETIC VALIDATION DATASET GENERATOR — not real logged data.
#
# Aiden's real Unified_logger.ino / lap_sim.py pipeline is confirmed working end-to-end
# (real ride: unified.csv, 115s, 223 rows). This script generates a physically-modeled
# synthetic ride -- a car driving three laps around a rectangular city block -- in the exact
# same CSV schema the real logger produces, so the pipeline can be validated against denser,
# cleaner data while field data collection is paused (leg injury).
#
# Every row here is derived from a kinematic model (speed profile from a corner-radius /
# friction-limited cornering-speed calc, longitudinal accel from dv/dt, lateral accel from
# v^2/r), not measured. Keep this file and its output (synthetic_ride.csv) clearly labeled
# and never merge it into unified.csv or represent it as a real logged ride.
#=========================================================================

import numpy as np
import math
import csv

# ---- Block geometry: rectangular loop, rounded corners (realistic street turning radius) ----
BLOCK_LENGTH = 120.0   # m, long side
BLOCK_WIDTH  = 80.0    # m, short side
CORNER_R     = 6.0     # m, corner turning radius (typical residential intersection)
N_LAPS       = 3

# ---- Driving parameters (casual residential driving, not a race) ----
CRUISE_SPEED = 9.0      # m/s, ~20 mph
MU           = 0.35     # target lateral g for a CASUAL residential turn (not tire-limit)
G            = 9.81
CORNER_SPEED = math.sqrt(MU * G * CORNER_R)   # v^2 = mu*g*r
A_ACCEL      = 2.0      # m/s^2, casual acceleration
A_BRAKE      = 3.0      # m/s^2, casual braking

# ---- GPS reference point (reuse the real logger's location for geographic continuity) ----
LAT_REF = 33.099426
LNG_REF = -96.092132
MPD_LAT = 111320.0
MPD_LNG = 111320.0 * math.cos(math.radians(LAT_REF))

# ---- Logger cadence (matches real Unified_logger.ino: ~515ms between rows) ----
DT_NOMINAL_MS = 515
DT_JITTER_MS  = 10   # +/- jitter, matching real hardware timing variance

rng = np.random.default_rng(42)

def build_path():
    """Builds a rounded-rectangle centerline path as (x, y, s, curvature, turn_sign) samples,
    finely spaced by arc length."""
    half_L = BLOCK_LENGTH / 2
    half_W = BLOCK_WIDTH / 2
    r = CORNER_R

    # Centerline of a rounded rectangle, built as 4 straights + 4 quarter-circle arcs,
    # traversed counter-clockwise starting at the midpoint of the bottom edge.
    segments = []  # each: ('straight', length) or ('arc', radius, angle_span)
    straight_L = BLOCK_LENGTH - 2 * r
    straight_W = BLOCK_WIDTH - 2 * r
    for _ in range(4):
        segments.append(('straight', straight_L if _ % 2 == 0 else straight_W))
        segments.append(('arc', r, math.pi / 2))

    # Walk the segments to build a dense (x, y) polyline
    x, y, heading = 0.0, -half_W, 0.0  # start at bottom edge midpoint-ish, heading +x
    xs, ys, curv, turn = [x], [y], [0.0], [0.0]
    ds = 0.25  # m, sample spacing along the path
    for seg in segments:
        if seg[0] == 'straight':
            length = seg[1]
            n = max(int(length / ds), 1)
            for _ in range(n):
                x += ds * math.cos(heading)
                y += ds * math.sin(heading)
                xs.append(x); ys.append(y); curv.append(0.0); turn.append(0.0)
        else:
            _, radius, span = seg
            n = max(int((radius * span) / ds), 1)
            dtheta = span / n
            # center of the arc is 90 deg to the left of current heading (CCW loop)
            cx = x - radius * math.sin(heading)
            cy = y + radius * math.cos(heading)
            start_ang = math.atan2(y - cy, x - cx)
            for i in range(1, n + 1):
                ang = start_ang + dtheta * i
                x = cx + radius * math.cos(ang)
                y = cy + radius * math.sin(ang)
                heading += dtheta
                xs.append(x); ys.append(y); curv.append(1.0 / radius); turn.append(1.0)

    xs, ys, curv, turn = map(np.array, (xs, ys, curv, turn))
    dx = np.diff(xs); dy = np.diff(ys)
    seg_len = np.sqrt(dx ** 2 + dy ** 2)
    s = np.concatenate([[0.0], np.cumsum(seg_len)])
    return xs, ys, s, curv, turn


def speed_profile(s, curv):
    """Forward/backward pass, same concept as lap_sim.py's final_velocity(): grip-limited
    cornering speed capped by cruise speed, with accel/brake ramps between."""
    n = len(s)
    ds = np.diff(s, prepend=s[0])
    ds[0] = ds[1] if n > 1 else 1.0

    v_limit = np.full(n, CRUISE_SPEED)
    v_limit[curv > 0] = CORNER_SPEED

    v_fwd = v_limit.copy()
    for i in range(1, n):
        v_possible = math.sqrt(max(v_fwd[i - 1] ** 2 + 2 * A_ACCEL * ds[i], 0.0))
        v_fwd[i] = min(v_possible, v_limit[i])

    v_bwd = v_limit.copy()
    for i in range(n - 2, -1, -1):
        v_possible = math.sqrt(max(v_bwd[i + 1] ** 2 + 2 * A_BRAKE * ds[i + 1], 0.0))
        v_bwd[i] = min(v_possible, v_limit[i])

    return np.minimum(v_fwd, v_bwd)


def main():
    xs, ys, s, curv, turn = build_path()
    v = speed_profile(s, curv)
    lap_length = s[-1]

    # Repeat for N_LAPS, offsetting arc length and unwrapping time by integrating ds/v
    all_x, all_y, all_v, all_curv, all_turn = [], [], [], [], []
    for lap in range(N_LAPS):
        all_x.append(xs); all_y.append(ys); all_v.append(v)
        all_curv.append(curv); all_turn.append(turn)
    all_x = np.concatenate(all_x); all_y = np.concatenate(all_y)
    all_v = np.concatenate(all_v); all_curv = np.concatenate(all_curv)
    all_turn = np.concatenate(all_turn)
    all_s = np.concatenate([s + lap * lap_length for lap in range(N_LAPS)])

    # Integrate time from arc length and speed (dt = ds/v)
    ds_full = np.diff(all_s, prepend=all_s[0]); ds_full[0] = ds_full[1]
    dt_full = ds_full / np.maximum(all_v, 0.3)
    t_full = np.cumsum(dt_full)
    t_full -= t_full[0]

    # Resample onto the logger's real cadence (~515ms, +/- jitter) via interpolation
    total_time = t_full[-1]
    n_rows = int(total_time / (DT_NOMINAL_MS / 1000.0))
    t_samples = [0.0]
    for _ in range(n_rows):
        dt = (DT_NOMINAL_MS + rng.uniform(-DT_JITTER_MS, DT_JITTER_MS)) / 1000.0
        t_samples.append(t_samples[-1] + dt)
    t_samples = np.array(t_samples)
    t_samples = t_samples[t_samples <= total_time]

    x_s = np.interp(t_samples, t_full, all_x)
    y_s = np.interp(t_samples, t_full, all_y)
    v_s = np.interp(t_samples, t_full, all_v)
    curv_s = np.interp(t_samples, t_full, all_curv)
    turn_s = np.interp(t_samples, t_full, all_turn) > 0.5

    # Longitudinal accel from dv/dt (vehicle frame), lateral accel from v^2 * curvature
    dv = np.gradient(v_s, t_samples)
    a_x = dv / G
    a_y = (v_s ** 2 * curv_s) / G
    a_y = np.where(turn_s, a_y, 0.0)
    # Small realistic sensor noise, matching the real logger's idle-noise magnitude (real
    # unified.csv shows ~+/-0.02g noise at rest: x_g=0.02, y_g=-0.04 while stationary)
    a_x += rng.normal(0, 0.015, size=len(a_x))
    a_y += rng.normal(0, 0.015, size=len(a_y))
    z_g = 1.0 + rng.normal(0, 0.01, size=len(a_x))

    lat = LAT_REF + y_s / MPD_LAT
    lng = LNG_REF + x_s / MPD_LNG
    lat = np.round(lat, 6)
    lng = np.round(lng, 6)

    time_ms = np.round(t_samples * 1000).astype(int) + 1000  # offset like a real millis() start

    out_path = "synthetic_ride.csv"
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time", "lat", "lng", "x_g", "y_g", "z_g"])
        for i in range(len(t_samples)):
            w.writerow([time_ms[i], f"{lat[i]:.6f}", f"{lng[i]:.6f}",
                        f"{a_x[i]:.2f}", f"{a_y[i]:.2f}", f"{z_g[i]:.2f}"])

    print(f"Wrote {len(t_samples)} rows to {out_path}")
    print(f"Total distance: {all_s[-1]:.1f} m over {N_LAPS} laps, duration {total_time:.1f} s")
    print(f"Max |a_x|: {np.max(np.abs(a_x)):.2f} g, Max |a_y|: {np.max(np.abs(a_y)):.2f} g")


if __name__ == "__main__":
    main()
