import serial
import time
import numpy as np
import threading

current_csi_data_x=[]
current_csi_data_y=[]

ser_x=serial.Serial(port="COM3",baudrate=115200,timeout=1)
ser_y=serial.Serial(port="COM4",baudrate=115200,timeout=1)


def get_csi_data_x():
    global current_csi_data_x
    return current_csi_data_x
def get_csi_data_y():
    global current_csi_data_y
    return current_csi_data_y

def read_csi_from_serial(axis):
    global ser_x,ser_y
    if axis=="x":
        ser=ser_x
    elif axis=="y":
        ser=ser_y
    else:
        raise ValueError("Invalid axis")
    while True: #read until valid data is obtained
        try:
            line=ser.readline().decode("utf-8").strip()
            if line.startswith("CSI_DATA"):
        except UnicodeEncodeError as e:
            print(e)
            continue

    global current_csi_data_x
    global current_csi_data_y
    ser=serial.Serial(port="COM3",baudrate=115200,timeout=1)
    while True:
        try:
            line=ser.readline().decode("utf-8").strip()
            if line.startswith("CSI_DATA_X:"):
                current_csi_data_x=[int(i) for i in line.split(":")[1].split()]
            elif line.startswith("CSI_DATA_Y:"):
                current_csi_data_y=[int(i) for i in line.split(":")[1].split()]
        except Exception as e:
            print(e)
            pass
        time.sleep(0.1)

def start_CSI_obtainer():
