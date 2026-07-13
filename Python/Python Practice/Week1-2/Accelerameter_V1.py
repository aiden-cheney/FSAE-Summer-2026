import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/aiden/OneDrive/Documents/Summer Project/Python/Python Practice/accel.csv')

df["time"] = df["time"]/1000
plt.plot(df["time"], df["x_g"], color="red", label="x_g")
plt.plot(df["time"], df["y_g"], color="green", label="y_g")
plt.plot(df["time"], df["z_g"], color="blue", label="z_g")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (g)")
plt.title("Accelerometer Data")
plt.legend()
plt.show()
