#basic list 
speeds = [30,45,25,60,35]

print (speeds[0]) #first item
print (speeds[-1]) #last item 
print (len(speeds)) #how many items 


#numpy and interprating laptime data
import numpy as np 

speeds = np.array([30,45,25,60,35])

print (speeds*2) #doubles evry speed 
print (speeds.mean()) #average speed
print(speeds.max()) #fastest corner 


#two arrays at once 
distances = np.array ([100,150,80,200,120])
speeds = np.array ([30,45,25,60,35])

times = distances / speeds
print (np.round(times,2))
print(f"Total time:{times.sum():.2f} seconds")

#plot with matplotlib

import matplotlib.pyplot as plt 

#create range of numbers from 0 to ten (basiaclly saying guve me 100 space numbers between 1 and 10)
x = np.linspace (0,10,100)

#calulate sin wave 
y = np.sin(x)

#plot it 
plt.plot (x,y)
plt.title ("sin Wave")
plt.xlabel ("X")
plt.ylabel ("Y")
plt.show ()