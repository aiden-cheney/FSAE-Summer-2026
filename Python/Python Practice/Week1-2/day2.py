# #for loop
# for i in range(5):
#     print(i)

# #while loop 
# x = 0 
# while x < 8:
#     print (x)
#     x+=1

# #function
# def add_numbers (a, b):
#     return a + b 

# result = add_numbers(3, 4)
# print(result)

#list of all corner speeds: 
corner_speeds = [30,45,50,60,35]

def calculate_lap_time(speeds):
    total_time = 0 
    for speed in speeds:
        time = 100 / speed # time = distance/ speed 
        total_time += time 
    return total_time

lap_time = calculate_lap_time(corner_speeds)
print (f"Estimated lap time: {lap_time:.2f} seconds")