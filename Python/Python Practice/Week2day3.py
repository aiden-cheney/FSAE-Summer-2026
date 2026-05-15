import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# # mass of our FSAE car in kg
# masslight = 300
# massheavy = 450

# # create a range of accelerations from 0 to 20 m/s²
# acceleration = np.linspace(0, 20, 100)

# # calculate force at each acceleration using F = ma
# forcelight = masslight * acceleration
# forceheavy = massheavy * acceleration
# # plot force vs acceleration
# plt.plot(acceleration, forcelight, color="blue", label="Light Car")
# plt.plot(acceleration, forceheavy, color="red", label="Heavy Car")

# # labels and title
# plt.title("Force vs Acceleration - FSAE Car")
# plt.xlabel("Acceleration (m/s²)")
# plt.ylabel("Force (N)")

# # add grid and legend
# plt.legend()
# plt.grid(True)

# plt.show()

theta = np.linspace(0, 2 * np.pi, 100)

x = np.cos(theta)
y = np.sin(theta)
xg = x *1.5
yg= y*1.5
plt.plot(xg, yg, color="purple", label="Circle")
plt.axhline(0, color="black", linestyle="--")
plt.axvline(0, color="black", linestyle="--")
plt.title("Friction circle")
plt.xlabel("Lateral acceleration (m/s²)")
plt.ylabel("Longitudinal acceleration (m/s²)")
plt.axis("equal")
plt.legend()
plt.grid(True)
plt.show()
