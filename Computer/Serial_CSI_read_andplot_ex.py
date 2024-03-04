import serial
import matplotlib.pyplot as plt
import numpy as np
import asyncio
from collections import deque
import time
import math

start_time=time.time()

def get_time():
    return time.time()-start_time

# # Open serial port
# ser = serial.Serial('COM8', 921600)

# # Read data from serial port
# while True:
#     try:
#         line = ser.readline().decode().strip()  # Read a line and decode it from bytes to string
#         if line.startswith("CSI_DATA"):
#             # Extract the array of values from the line
#             data_str = line.split(",")[-1]  # Get the last part of the line which contains the array
#             data_str = data_str[1:-1]  # Remove brackets from the array
#             data_values = [int(x) for x in data_str.split()]  # Convert the space-separated string into a list of integers
#             print("Received data:", data_values)  # Do whatever analysis or processing you need with the data
#     except UnicodeDecodeError as e:
#         print("Error decoding line:", e)
#         continue
#     except KeyboardInterrupt:
#         print("Exiting...")
#         break

# # Close serial port
# ser.close()
def csi_to_features(csi_data):
    features=[]
    csi_data=np.array(csi_data)
    array_length=csi_data.shape[0] #or .size
    
    #use sd scope of 20
    # sd_sampling_range = 20
    # for i in range(0,array_length-sd_sampling_range):
    #     sd_value= np.std(csi_data[i:i+sd_sampling_range])
    #     features.append(sd_value)
    # return features
        
    #It seems to be some odd operation that is not sd
    #It is root mean square RMS ok
    sampling_range=10
    mean_val=csi_data.mean()
    for i in range(0,array_length-sampling_range):
        vals=[]
        for j in range(i,i+sampling_range):
            val=math.pow(csi_data[j]-mean_val,2)
            vals.append(val)
        val_append=math.sqrt(sum(vals)/sampling_range)
        features.append(val_append)
    return features

ser = serial.Serial('COM8', 921600) #pink
# ser = serial.Serial('COM16', 921600) #yellow
plt.ion()
fig, ax = plt.subplots()

ax.set_ylim(-100, 100)
ax.set_title('Real-time CSI data')
ax.set_xlabel('index')
ax.set_ylabel('CSI Value')
line_n=0;

line_=None;
period=0.5;
period_tick=get_time()/period;
while True:
    try:
        line = ser.readline().decode().strip()  # Read a line and decode it from bytes to string
        if line.startswith("CSI_DATA"):
            line_n+=1
            print(line_n)
            # Extract the array of values from the line
            data_str = line.split(",")[-1]  # Get the last part of the line which contains the array
            data_str = data_str[1:-1]  # Remove brackets from the array
            data_values = [int(x) for x in data_str.split()]  # Convert the space-separated string into a list of integers
            # data_values = csi_to_features(data_values)
            # print("Received data:", data_values)  # Do whatever analysis or processing you need with the data

            nperiod_tick=get_time()/period
            if nperiod_tick>period_tick:
                period_tick=nperiod_tick
                if line_==None:
                    print("first time")
                    line_, = ax.plot(data_values)
                else:
                    line_.set_ydata(data_values)
                plt.draw()
                plt.pause(0.01)
            # ser.flushInput()
            # ser.flushOutput()
    except UnicodeDecodeError as e:
        print("Error decoding line:", e)
        continue
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except ValueError as e:
        print("ValueError")
        continue
    