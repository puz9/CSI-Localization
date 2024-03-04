import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sn
import scipy.io as sio
import os
import serial


def plot_heatmap(data):
    sn.heatmap(data, cmap='coolwarm', cbar=True)
    plt.title('Heatmap of Features')
    plt.xlabel('Feature Index')
    plt.ylabel('Sample Index')
    plt.show()

heatmap_data = np.zeros((1, 20))  # Assuming 20 features
def update_heatmap(features):
    global heatmap_data
    heatmap_data = np.vstack((heatmap_data, features))
    heatmap_data = heatmap_data[-50:]  # Keep only last 50 rows for real-time visualization

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

ser = serial.Serial('COM8', 921600)
while True:
    try:
        line=ser.readline().decode().strip()
        if line.startswith("CSI_DATA"):
            data_str=line.split(",")[-1]
            data_str=data_str[1:-1]
            data_values=[int(x) for x in data_str.split()]
            features=csi_to_features(data_values)
            print(features)
    except UnicodeDecodeError as e:
        print("Error decoding line:", e)
        continue
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except ValueError as e:
        print("ValueError")
        continue
    