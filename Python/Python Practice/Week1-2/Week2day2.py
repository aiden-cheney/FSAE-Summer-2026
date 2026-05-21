import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# #here we are crating 10 track postion eveny  spaced fomr 0 to 100 meters using linspase 
# track_position = np.linspace(1,100,10)
# print (track_position)

# # dot product multiplies two arrays element by element then sums them
# # example: calculating total work done on the car
# force = np.array([100, 200, 150, 300, 250])    # force in Newtons at each point
# distance = np.array([10, 20, 15, 30, 25])       # distance in meters at each point

# # work = force x distance at each point added together
# work = np.dot(force, distance)
# print(f"Total work done: {work} Joules")

# # array math - do math on every element at once
# speeds = np.array([30, 45, 25, 60, 35])         # speeds in mph

# # convert every speed to m/s in one line (1 mph = 0.447 m/s)
# speeds_ms = speeds * 0.447
# print(f"Speeds in m/s: {np.round(speeds_ms, 2)}")


# linspace_prac = np.linspace(0,500, 50)
# mass = np.array([200,380,210,400,175])
# acceleration = np.array([10,20,45,50,80])
# force = mass*acceleration
# # print (linspace_prac)
# print (force)

data = {
    "speed": [30, 45, 25, 60, 35],           # speed in mph
    "time": [20,15, 15, 20, 10],        # time
}

df = pd.DataFrame(data)

# plot speed vs time
plt.plot(df["speed"],df["time"], color="green", label="Speed vs Time Graph")
plt.xlabel("Speed (mph)")
plt.ylabel("Time (s)")
plt.show()