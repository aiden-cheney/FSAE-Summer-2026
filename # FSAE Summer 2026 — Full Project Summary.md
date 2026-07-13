# FSAE Summer 2026 — Full Project Summary
## Aiden Cheney | UT Austin FSAE Unsprung Dynamics
### github.com/Aiden-Cheney/FSAE-Summer-2026 | Hard end date: July 14, 2026

---

## What This Project Is

An 11-week self-directed summer engineering project running three parallel tracks: a Python lap time simulator, a unified Arduino data logger, and a billet front upright taken through a full design → FEA → CAM loop. The project was originally 14 weeks and was compressed to 11 to allow time for a second opportunity — a drone startup collaboration with students from Harvard and Michigan beginning after July 14th.

The overarching goal is not to produce deliverables. It is to develop genuine mechanical engineering intuition — force path reasoning, material behavior, geometry and stress, and the physical meaning behind every number the simulator produces. Every session is structured so that Aiden explains concepts physically in plain English before any implementation happens. The code and CAD are tools for testing understanding, not replacing it.

---

## Track 1: Python Lap Time Simulator

### What's been built

The simulator lives in `lap_sim.py` and `tire_model_pacejka.py`. It is a point-mass lap time simulator built from scratch over eight weeks, starting from zero Python knowledge.

**Foundation (weeks 1-2):** Learned numpy, pandas, matplotlib, scipy. Built a friction circle, plotted real Arduino accelerometer data, learned F=ma as the physical skeleton of the simulator.

**Vehicle dynamics theory (weeks 3-4):** Built `weight_transfer.py` — calculates lateral and longitudinal weight transfer using ΔW = (m × a × g × h) / trackwidth. At 1.5g lateral, a 300kg car transfers ~551N to the outside tires. Built `tire_model.py` — linear model F = Cα × α with cornering stiffness 800 N/deg, valid to ~3° slip angle. Built `dynamics_dashboard.py` combining weight transfer, friction circle, and real Arduino bike data. Learned slip angle physically — it is the angle between where the wheel points and where it travels, caused by rubber deformation. Understeer is front losing grip first, oversteer is rear losing grip first. Learned trail braking as the physical act of moving around the friction circle boundary.

**Track map and speed profile (weeks 3-4 continued):** Represented the track as X/Y coordinates — synthetic FSAE oval: x = 40cos(t) + 5cos(2t), y = 20sin(t). Calculated curvature using numpy differential geometry (dx, dy, ddx, ddy). Derived v_max = sqrt(g_limit × 9.81 / curvature) from circular motion physics. Implemented forward pass (v_next = sqrt(v² + 2 × a_max × ds)) and backward pass (same formula working backward with braking deceleration). Final speed at each point = minimum of forward and backward.

**Full physics stack (weeks 5-6):** Discovered ds = 1m was wrong for a parametric track. Calculated real arc length: sum(sqrt(dx² + dy²)) = 195.35m, ds = 0.39m per step. Built lap_time() function: dt = ds / v_final summed across all track points. Added engine power limit: a_power = P/(m×v) computed at each step inside the forward pass loop, a_actual = min(a_power, a_max). Added aero drag: F = 0.5 × rho × v² × Cd × A, subtracted in forward pass, added to effective braking in backward pass. Added downforce using team CL = 2.52 from Orion Suspension Master spreadsheet: g_limit_effective = g_limit + F_downforce/(m×9.81), v_max_effective = sqrt(g_limit_effective × 9.81 / curvature). All three downforce lines run as numpy array operations with no loop. Built mass sensitivity study using for loop over np.arange(200, 450, 25) — curve is nonlinear because mass appears in the denominator of the power equation. Loaded unified.csv GPS data, filtered duplicate header rows, calculated g_total = sqrt(x_g² + y_g²) excluding z (contains gravity, not part of friction circle plane), plotted GPS path color-coded by g_total using 'hot' colormap.

Lap time progression: 10.11s (base) → 10.18s (power limit added) → 10.28s (drag added) → 9.98s (downforce added).

**Pacejka tire model (weeks 7-8):** Implemented Pacejka Magic Formula from scratch in `tire_model_pacejka.py`: Fy = D × sin(C × arctan(B×α − E×(B×α − arctan(B×α)))). Coefficients for Hoosier R25B: B = 10.0, C = 1.9, D = 2800N, E = -1.5. Key bug caught and fixed: alpha must be in radians inside the equation — input array stays in degrees for plotting, fix was alpha_rad = np.deg2rad(alpha). Bug was caught by recognizing a physically impossible spike shape on the plot — physical intuition, not just debugging. Plotted at three normal loads (light D=1800, nominal D=2800, heavy D=3600) to demonstrate load sensitivity: outside tire gains less grip than inside loses, net result is a rolling car has less total grip than a static one. Integrated Pacejka into lap_sim.py as cornering limit: peaklatforce = np.max(Fy), g_limit = peaklatforce / (m × g). Lap time increased from 9.98s to 11.80s — this is more accurate, not worse. The original 1.5g assumed 4414N lateral force; Pacejka shows the tire peaks at 2800N (~0.95g). Implemented combined slip using friction ellipse: Fy_combined = peaklatforce × sqrt(1 − (Fx / Fx_max)²), Fx_max = 3200N. Updated friction circle to friction ellipse plotted in all four quadrants in g-units. Real Arduino bike data overlaid — all points inside the boundary as expected for casual riding (~0.73g max).

**Current dashboard — 8 active subplots in a 3×3 layout:**
- ax1: weight transfer (lateral + longitudinal)
- ax2: friction ellipse with Arduino bike data overlay
- ax3: lateral force vs slip angle (linear, clipped, Pacejka)
- ax4: track map with lap time and length overlay
- ax5: track curvature vs position
- ax6: velocity vs position (grip limit + final velocity)
- ax7: lap time vs mass sensitivity study
- ax8: GPS path color-coded by g-force magnitude
- ax9: hidden

**Current lap_sim.py parameters:**
- m = 300 kg
- g_limit = 0.95 (derived from Pacejka, was hardcoded 1.5)
- a_max = 10 m/s², b_max = 15 m/s²
- power = 60,000 W
- rho = 1.225 kg/m³, Cd = 1.5, CL = 2.52, area = 1.0 m²
- Fx_max = 3200 N
- Track: synthetic FSAE oval, 195.35m, ds = 0.39m
- Final lap time: 11.80s

**Key physics concepts understood:**
- Pacejka B controls initial slope (stiffness), C controls curve shape, D is peak force, E controls behavior past the peak (usually negative, causes dropoff)
- BCD = cornering stiffness at zero slip — sanity check against linear model
- Load sensitivity: grip doesn't scale linearly with normal load, effective grip coefficient drops as load increases
- Combined slip: tire has a finite grip budget split between lateral and longitudinal forces, trail braking is deliberately moving around the ellipse boundary
- Point-mass sim limitations: fixed g_limit everywhere on track, assumes perfect driver always at tire peak, no dynamic weight transfer connected to tire model, no instantaneous slip angle tracking — biggest missing physics is weight transfer feeding Pacejka normal load

**What's still to do on the Python track:**
- Load real GPS track from unified.csv into lap_sim.py, replace synthetic oval with a track Aiden actually rode
- Compare sim speed trace to real logged GPS speed on the same plot
- Sensitivity study on the real GPS track (lap time vs mass, vs CL)
- Final code cleanup, hero output figure, GitHub README

---

## Track 2: Arduino Data Logger

### Status: COMPLETE as of week 6

**Hardware:** Arduino Uno R3, MPU-6050 accelerometer/gyroscope, NEO-6M GPS module, micro SD card module, 32GB microSD, USB power bank for standalone operation.

**What was built:** Three progressive sketches culminating in a unified logger combining all three modules with no conflicts between SPI (SD card on pins 10-13), I2C (MPU on A4/A5), and SoftwareSerial (GPS on pins 2/3). Logs one row every 500ms to unified.csv with headers: time, lat, lng, x_g, y_g, z_g.

**Hardware issues debugged:** Bad MPU-6050 solder joints identified via I2C scanner (no devices found → resoldered → device found at 0x68). TX/RX crossover rule confirmed. Library conflict resolved by switching from default SD library to SdFat by Bill Greiman.

**Real data collected:** 115-second bike ride logged 223 data points. Data showed negative x_g (braking) and positive y_g (turning left). GPS fix achieved at 33.099426, -96.092132, confirmed correct for Greenville TX. Lateral accelerations up to -0.73g, braking events up to -0.61g. All points inside the friction ellipse boundary as expected for casual riding. Multiple power cycles created duplicate header rows in CSV — handled in Python with df[df['lat'] != 'lat'] filter.

**Key concepts understood:** I2C communication (SDA/SCL, address 0x68), SPI communication (MISO/MOSI/SCK/CS), SoftwareSerial to avoid hardware serial conflict, GPS cold start requiring 4+ satellite line of sight, 16384 raw units = 1g at ±2g range, TX/RX crossover rule.

---

## Track 3: Billet Front Upright — SolidWorks → ANSYS → CAM

### What this is

A brand-new billet front upright designed from scratch using team pickup point constraints from the Orion Suspension Master spreadsheet. Not a redesign of the existing part — the existing part is reference only for packaging logic. The design is constrained by real team hardpoints and must interface with the real car.

### What's been built

**Bearing bore datum (week 5 weekend):** Bearing bore centerline located at Y=22 inches from car centerline — distinct from wheel centerline at Y=24 inches; the hub bridges the 2-inch gap. Bore diameter 2.835 inches, housing depth 31mm, snap ring groove width 2.66mm, inboard groove start 0.591 inches from inboard face. Boss extruded 31mm deep centered on midplane, one snap ring groove cut at correct offset, mirrored across midplane for symmetry. This is the datum — everything else locates off it.

**Control arm mounts (week 5 weekend):** Upper control arm mount lofted from bearing bore housing to pickup point at Z=10.551 inches, 0.150 inch wall thickness. Lower control arm mount lofted to Z=4.488 inches, 0.125 inch wall thickness. Upper is heavier than lower because the upper ball joint sees greater cornering force due to its longer moment arm from the contact patch.

**Steering arm (week 5 weekend):** Double-shear clevis pickup for tie rod. Double shear chosen over single shear to eliminate bending moment on the joint bolt.

**Force path analysis (week 6):** Worked through all four load cases with feedback from James Totat, senior mechanical engineer. Lateral cornering: force enters at bearing bore, splits between upper and lower ball joints, upper carries more due to moment arm. Braking: longitudinal force at bore, braking torque reacts through caliper mount bosses in shear directly into bore housing wall. Combined: worst case, all load paths active simultaneously. Bearing bore wall identified as highest stress region in every single load case — the only point where all forces converge. This finding directly informs FEA expectations.

**Design philosophy established:** Triangulated rib structure over organic lofted geometry, per James Totat's feedback. Material in direct tension/compression rather than bending. Every feature must have a structural reason. Mental model: diamond shape with bearing bore at center and pickup points at vertices.

**Caliper mount (weeks 7-8):** Two bolt bosses positioned approximately 60° above and below the bearing bore centerline. Lower mount uses a triangulated rib for direct load path to the bore wall. Upper mount uses lofted geometry — accepted for now, flagged for potential review after FEA. Single shear configuration matches the existing UT FSAE upright (team-validated decision). Force path traced and confirmed before modeling: caliper clamps rotor → braking torque reacts through mount bolts in shear → into upright body → through triangulated ribs → bearing bore wall → control arm pickups → chassis.

**Still to do before ANSYS:**
- Wheel speed sensor mounts
- Full geometry review — every feature justified against load path or packaging, remove anything that isn't
- Mass estimate using material density and mental volume model (target within 20% of what ANSYS reports)
- Geometry lock

**FEA plan (weeks 9-10):**
- Before importing to ANSYS, Aiden must describe the full combined cornering and braking load path from memory
- Import upright, apply load cases using force magnitudes derived from lap sim output
- Load cases: cornering (lateral force at hub), braking (longitudinal force at caliper mount), combined worst case
- Record mass, peak stress, max deflection
- Predict stress location before solving — compare prediction to actual result
- Iterate: add material where stress is too high, remove where it is low
- Build a table: iteration by iteration tracking mass, peak stress, deflection
- Target two to three FEA iterations

**CAM plan (weeks 10-11):**
- Set up stock (billet block), part zero, and work coordinate system in SolidWorks CAM
- Think through number of setups — uprights typically need 3-4 sides, sketch fixturing on paper first
- Set up machining operations: facing pass on bearing bore face, contour pass on upright body, bore cycle for the bearing bore
- Run simulation, check for gouges and collisions
- If CAM reveals geometry that's hard to machine (internal corners too tight, undercuts), revise geometry and run a final ANSYS pass
- Goal: clean, collision-free simulation — Aiden is not sending this to a machine, but the simulation should be manufacturable

---

## Current Repository Structure

```
FSAE-Summer-2026/
├── Python/
│   └── Python Practice/
│       ├── Week3-4/
│       │   ├── lap_sim.py (full dashboard, 8 subplots)
│       │   ├── weight_transfer.py
│       │   ├── tire_model.py (linear)
│       │   ├── dynamics_dashboard.py
│       │   └── track_map.py
│       ├── tire_model_pacejka.py (weeks 7-8)
│       ├── unified.csv (real GPS + accelerometer ride data)
│       └── accel.csv (early accelerometer data, 223 rows)
└── Arduino/
    └── Arduino Files/
        └── Practice/
            ├── GPS_v1/
            ├── Unified_Logger_v1/
            ├── Program_1/ through Program_3/
            ├── First_LED_Circuit/
            ├── First_datalog/
            ├── MPU_v1/
            └── SD_Reader_v1/
```

---

## Remaining Schedule — Weeks 9-11

### Week 9
- SolidWorks: wheel speed sensor mounts, full geometry review, mass estimate, geometry lock
- ANSYS: import upright, set up load cases from lap sim force magnitudes, predict stress location before solving, first FEA run, record results
- Python: load real GPS track from unified.csv into lap_sim.py, compare sim speed trace to real GPS speed

### Week 10
- ANSYS: first design iteration based on results — add material at stress concentrations, remove at low-stress regions
- ANSYS: second run, compare to first, build iteration table
- SolidWorks CAM: set up stock and part zero, plan setups, first toolpath operations
- Python: sensitivity study on real GPS track, lap time vs mass and CL, predict before running

### Week 11 (July 7-18, hard stop July 14)
- SolidWorks CAM: complete all toolpath setups, run full simulation clean, address any geometry changes CAM reveals
- Final ANSYS pass after any CAM-driven geometry changes
- Python: final code cleanup, hero output figure (track map + speed trace + g-force trace + lap time in one figure), GitHub README
- Upright design report: 1-2 pages covering design constraints, design decisions, FEA iteration table, mass comparison, CAM analysis and setup count, manufacturability notes
- Resume bullets and LinkedIn update
- Informal presentation to FSAE team

---

## What This Project Should Produce

Three finished, documented deliverables:

**1. Python lap time simulator** — modular, documented codebase with Pacejka tire model, aero physics, real GPS track input, sensitivity analysis, and an 8-subplot dashboard. On GitHub with a full README. Demonstrates Python proficiency, vehicle dynamics knowledge, and real data analysis.

**2. Unified Arduino data logger** — complete hardware build, real outdoor data collected, data pipeline into Python confirmed. Demonstrates hardware debugging, embedded C, sensor fusion, and the ability to build a real measurement system.

**3. Billet front upright** — designed from scratch against real team pickup points, iterated through at least two FEA runs, CAM simulation complete and collision-free. Demonstrates force path reasoning, SolidWorks proficiency, ANSYS FEA workflow, and manufacturing awareness. Full design report documenting the engineering decisions.

**What Aiden should walk away with:** The ability to look at a physical system and reason about where forces go and where things will fail. The intuition to look at an FEA stress plot and know whether it makes sense before trusting it. A working understanding of what tire and suspension parameters actually mean for how a car behaves at the limit. And a GitHub repository and portfolio that tells a coherent engineering story from sensor to simulation to machined part.

---

## Key Numbers to Know

- Lap time: 11.80s (Pacejka model) vs 9.98s (hardcoded 1.5g) — difference reflects ~0.95g real tire peak vs assumed 1.5g
- Track: 195.35m, ds = 0.39m, synthetic FSAE oval
- Pacejka coefficients (Hoosier R25B): B=10.0, C=1.9, D=2800N, E=-1.5
- Peak lateral force: 2800N (~0.95g at 300kg)
- Longitudinal peak: Fx_max = 3200N
- Downforce: CL = 2.52 (team value, Orion spreadsheet)
- Bearing bore: 2.835in diameter, 31mm deep, Y=22in from car centerline
- Upper CA mount: Z=10.551in, 0.150in wall
- Lower CA mount: Z=4.488in, 0.125in wall
- MPU-6050 I2C address: 0x68, 16384 raw units = 1g
- GPS fix location: 33.099426, -96.092132 (Greenville TX)
- Max recorded acceleration: -0.73g lateral, -0.61g braking