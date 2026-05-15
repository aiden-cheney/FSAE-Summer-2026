import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

df = pd.read_csv('Python/Python Practice/data.csv')

print(df)

fig, (pl1, pl2) = plt.subplots(2, 1, figsize=(8, 8))

pl1.plot(df['speed'],df['time'], color="green", label="speed vs time")
pl1.set_xlabel('speed')
pl1.set_ylabel("time")
pl1.legend()
pl1.grid(True)

pl2.plot(df['acceleration'],df['time'], color="blue", label="acceleration vs time")
pl2.set_xlabel('acceleration')
pl2.set_ylabel("time")
pl2.legend()
pl2.grid(True)

plt.show()