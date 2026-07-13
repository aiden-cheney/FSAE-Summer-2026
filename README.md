# FSAE Summer 2026

Self-directed summer engineering project for UT Austin FSAE: a Python lap time simulator, a
unified Arduino data logger, and a billet front upright taken through design -> FEA -> CAM.
Built from scratch to develop real mechanical engineering intuition -- force paths, material
behavior, and the physical meaning behind every number a simulator or solver produces, not just
to produce deliverables.

## Python Lap Time Simulator

`Python/Python Practice/Week3-4/lap_sim.py` is the canonical simulator (consolidated 2026-07-11
from two development files into one). It models:

- **Weight transfer** (lateral + longitudinal) from CG height, trackwidth, and wheelbase.
- **A real Pacejka tire fit** — Hoosier 16x7.5-10, Round 9 TTC data @ 10psi, derated 0.75 for
  lab-to-track grip loss (B=20.85, C=1.411, D=4180N, E=-1.027).
- **A 4-tire load-sensitive grip limit** (`peak_lateral_g()`), solved self-consistently: lateral
  weight transfer shifts load to the outer tire pair, and tire mu drops as load increases, so
  the model captures the real grip loss from weight transfer rather than assuming a flat number.
- **Power, aerodynamic drag, and downforce** (team CL = 2.52) in a forward/backward velocity
  integration pass over a synthetic FSAE-oval track (195.35 m, real arc-length ds).
- **Combined-slip friction ellipse**, with real logged accelerometer data overlaid.
- **Sensitivity studies** — lap time vs. mass and vs. downforce coefficient (CL).
- **Real GPS overlay** from the Arduino logger's `unified.csv` (see below) — plotted alongside
  the sim, not yet used as a competitive-lap comparison (see limitations below).

Current result: **~10.3 s** estimated lap time on the synthetic track at 300 kg, CL = 2.52,
4-tire load-sensitive grip limit ~1.37 g. Run it: `python lap_sim.py` (needs numpy, pandas,
matplotlib; expects `unified.csv` at the path set in `UNIFIED_CSV`).

**Known limitations, stated plainly:**
- The real GPS log is a short, slow bike test ride (~5 minutes, only ~21 distinct resolved
  positions) — not a competitive FSAE lap. Sim lap time and the GPS log are not a like-for-like
  comparison yet; that needs a real competitive lap logged on the actual track.
- The GPS-derived speed series is dominated by fix-jitter (found 2026-07-11): with so few
  resolved positions, the module is mostly bouncing between nearby fixes rather than tracking
  continuous motion, so it's plotted for reference only, not treated as validated velocity data.
- It's a point-mass model: no per-corner dynamic weight transfer feeding the tire model in real
  time, and it assumes a driver always at the tire's peak grip.

### Synthetic validation dataset

`generate_synthetic_ride.py` generates `synthetic_ride.csv` — a physically-modeled synthetic
ride (a car driving three laps around a rectangular city block: corner-radius-limited cornering
speed, dv/dt-derived longitudinal accel, v²/r-derived lateral accel, realistic sensor noise) in
the exact same CSV schema the real logger produces. **This is simulated data, not a real logged
ride** — it exists to validate the GPS/accelerometer pipeline end-to-end against denser, cleaner
data while real field data collection is paused (injury). `lap_sim.py` plots it in a separate,
clearly-labeled figure (`synthetic_ride_dashboard.png`) — it is never merged into `unified.csv`
or presented as real logged data anywhere in this repo.

`Week5-6/Untitled-1.py` and `Week5-6/tire_model_pacejka.py` are earlier development files, kept
for history — both superseded by the canonical file above.

## Arduino Data Logger

`Ardiouno/Ardiono Files/Practice/Unified_logger/Unified_logger.ino` — complete. Logs GPS
(NEO-6M), accelerometer/gyro (MPU-6050, I2C 0x68), and SD card (SdFat, avoiding a library
conflict with the default SD library) to `unified.csv` every ~500 ms:
`time, lat, lng, x_g, y_g, z_g`. SPI (pins 10-13) for the SD card, I2C (A4/A5) for the MPU,
SoftwareSerial (pins 2/3) for the GPS, with no pin conflicts between the three.

Real data collected: a 115+ second ride, raw accelerometer readings consistent with real braking
and cornering (negative x_g under braking, positive y_g turning left), and a GPS fix confirmed
at a real logged location. Known data-quality issue: restarting the logger between power cycles
writes a duplicate header row into the CSV; handled downstream by filtering rows where
`lat == 'lat'`.

## Billet Front Upright (SolidWorks -> ANSYS -> CAM)

`Upright/` — CAD built from real team pickup-point constraints (not a redesign of the existing
part). FEA setup started in ANSYS; first solve and CAM work are still in progress.

## Status

Lap sim and logger are in a semi-finished state as of 2026-07-11 (physics consolidated into one
canonical file, real bugs found and documented rather than hidden). Upright FEA/CAM is the
remaining major work before the July 14 deadline.
