# --------SINE VS COSINE--------
#  import numpy as np 
# import matplotlib.pyplot as plt

# #create x values form 0 to 100
# x = np.linspace(0,10,100)

# #Create tow doffrent waves 
# sin_wave = np.sin(x)
# cos_wave = np.cos(x)

# #plotboth on the same figure with labels and colors 
# plt.plot(x, sin_wave, color="blue", label="Sin")
# plt.plot(x, cos_wave, color="red", label= "Cos")

# ##add titles and axs to labels 
# plt.title ("sin vs cos waves")
# plt.xlabel("X-Axis")
# plt.ylabel("Y-Axis")

# #add a legene so we know which line is whcih 
# plt.legend()

# #add grid 
# plt.grid(True)

# plt.show()


# ----------Force vs Acceel----------
# import numpy as np 
# import matplotlib.pyplot as plt

# #simulatign force vs acceration 
# mass = 300

# acceleration = np.linspace(0, 20,100)

# force = mass*acceleration

# #plotboth on the same figure with labels and colors 
# plt.axhline(y=mass, color="green", label="Mass (kg)")
# plt.plot(acceleration, force, color="blue", label= "Force (N)")

# ##add titles and axs to labels 
# plt.title ("FORCE VS ACCEL")
# plt.xlabel("Acceleration")
# plt.ylabel("Force")

# #add a legene so we know which line is whcih 
# plt.legend()

# #add grid 
# plt.grid(True)
# plt.xlim(left=0)
# plt.show()

# ----------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# create our track data
data = {
    "corner": [1, 2, 3, 4, 5],           # corner number
    "speed": [30, 45, 25, 60, 35],        # speed in mph
    "distance": [100, 150, 80, 200, 120]  # distance in feet
}

# create the dataframe
df = pd.DataFrame(data)

# calculate time and force for each corner
df["time"] = df["distance"] / df["speed"]
df["force"] = 300 * (df["speed"] / 10)   # simplified force calculation

# create a figure with 2 subplots stacked on top of each other
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# --- TOP GRAPH: bar chart of speed at each corner ---
ax1.bar(df["corner"], df["speed"], color="blue", label="Speed (mph)")
ax1.set_title(f"Speed at Each Corner — Lap Time: {df['time'].sum():.2f} seconds")
ax1.set_xlabel("Corner Number")
ax1.set_ylabel("Speed (mph)")
ax1.grid(True)
ax1.legend()

# --- BOTTOM GRAPH: force line graph ---
ax2.plot(df["corner"], df["force"], color="red", marker="o", label="Force (N)")
ax2.set_title("Force at Each Corner")
ax2.set_xlabel("Corner Number")
ax2.set_ylabel("Force (N)")
ax2.grid(True)
ax2.legend()

# make sure the graphs dont overlap
plt.tight_layout()

plt.show()