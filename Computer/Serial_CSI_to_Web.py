import json
import os
import time
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import train_test_split 
from sklearn.datasets import load_iris 
import joblib
import serial
import math
from collections import deque, Counter
import threading
import requests
import keyboard as kb

os.chdir(os.path.dirname(os.path.abspath(__file__)))

port_x = "COM8"
port_y = "COM20"


def normalize_raw_csi(raw_csi):
    return [v/128 for v in raw_csi]

def raw_csi_to_magnitudes(raw_csi):
    magnitudes = []
    if len(raw_csi) % 2 != 0:
        raw_csi = raw_csi[:-1]
    # Iterate through the raw CSI data by pairs
    for i in range(0, len(raw_csi), 2):
        # Extract the imaginary and real parts of the complex number
        imaginary = raw_csi[i]
        real = raw_csi[i + 1]
        # Calculate the magnitude of the complex number
        magnitude = math.sqrt(real**2 + imaginary**2)
        # Append the magnitude to the magnitudes array
        magnitudes.append(magnitude)
    return magnitudes

def normalize_magnitudes(magnitudes):
    return [v/(128*math.sqrt(2)) for v in magnitudes]

def raw_csi_to_phases(raw_csi):
    phases = []
    if len(raw_csi) % 2 != 0:
        raw_csi = raw_csi[:-1]
    # Iterate through the raw CSI data by pairs
    for i in range(0, len(raw_csi), 2):
        # Extract the imaginary and real parts of the complex number
        imaginary = raw_csi[i]
        real = raw_csi[i + 1]
        # Calculate the phase of the complex number
        phase = math.atan2(imaginary, real)
        # Append the phase to the phases array
        phases.append(phase)
    return phases

def raw_csi_to_features(csi_data_x,csi_data_y):
    # rx=normalize_raw_csi(csi_data_x)
    # ry=normalize_raw_csi(csi_data_y)
    if len(csi_data_x)==0:
        return []
    if len(csi_data_y)==0:
        return []
    rx=raw_csi_to_magnitudes(csi_data_x)
    ry=raw_csi_to_magnitudes(csi_data_y)
    # rx=normalize_magnitudes(rx)
    # ry=normalize_magnitudes(ry)
    features=rx+ry
    return features

knn = joblib.load('knn_model.pkl')
def predict_cell_index(csi_data_x,csi_data_y):
    global knn
    features=raw_csi_to_features(csi_data_x,csi_data_y)
    if len(features)==0:
        print("Not enough data")
        return 0
    return knn.predict([features])[0]
answers=deque(maxlen=10)
def get_map_data(csi_data_x,csi_data_y):#It is best to average the answer over a few frames

    next_cell_index=predict_cell_index(csi_data_x,csi_data_y)
    answers.append(next_cell_index)

    cell_index=Counter(answers).most_common(1)[0][0]    #get max count value

    map_r=[
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
    if cell_index==0:
        return map_r
    cell_index-=1
    map_r[cell_index//4][cell_index%4]=1
    return map_r

csi_data_x=[]
csi_data_y=[]

def read_serial_thread(ser,axis):
    global csi_data_x,csi_data_y
    while True:
        if kb.is_pressed("ctrl+c"):
            break
        try:
            if axis=="x":
                ser=ser_x
            else:
                ser=ser_y
            line = ser.readline().decode("utf-8").strip()
            print(line)
            if line.startswith("CSI_DATA"):
                data_str=line.split(",")[-1]
                data_str=data_str[1:-1].strip().split(" ")
                raw_csi_data = [int(x) for x in data_str]
                if axis=="x":
                    csi_data_x=raw_csi_data
                else:
                    csi_data_y=raw_csi_data
        except UnicodeDecodeError as e:
            print(e)
            continue
        except ValueError as e:
            print(e)
            continue
def upload_map_data_thread():
    global csi_data_x,csi_data_y
    try:
        while True:
            if kb.is_pressed("ctrl+c"):
                break
            map_data=get_map_data(csi_data_x,csi_data_y)
            response=requests.post("http://localhost:8000/upload_map_data",json={"map":map_data})
            if response.status_code==200:
                print(json.loads(response.text)["message"])
            else:
                print(response.text)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":

    ser_x = serial.Serial(port_x, 921600)
    ser_x.flushInput()
    ser_x.flushOutput()

    ser_y = serial.Serial(port_y, 921600)
    ser_y.flushInput()
    ser_y.flushOutput()


    try:
        t1=threading.Thread(target=read_serial_thread,args=(ser_x,"x"))
        t2=threading.Thread(target=read_serial_thread,args=(ser_y,"y"))
        t3=threading.Thread(target=upload_map_data_thread)
        t1.start()
        t2.start()
        t3.start()
        while True:
            pass
    except KeyboardInterrupt:
        ser_x.close()
        ser_y.close()
        print("Serial port closed")
        exit(0)