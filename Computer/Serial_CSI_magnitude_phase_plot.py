import serial
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time
import math

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

# Open serial port
try:
    ser = serial.Serial('COM16', 921600)
    ser.flushInput()
    ser.flushOutput()
except serial.SerialException as e:
    print("Error opening serial port:", e)
    exit(1)

# Initialize buffers
raw_csi_buffer = deque(maxlen=1000)  # Buffer to store raw CSI data
magnitude_buffer = deque(maxlen=1000)  # Buffer to store magnitudes
phase_buffer = deque(maxlen=1000)  # Buffer to store phases

# Create figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Plot settings
x = np.arange(0, len(raw_csi_buffer), 1)

# Update function for plotting
def update_plot():
    x = np.arange(0, len(raw_csi_buffer), 1)
    axs[0].cla()
    axs[0].plot(x, raw_csi_buffer)
    axs[0].set_title('Raw CSI Data')
    axs[0].set_xlabel('Index')
    # axs[0].set_ylabel('CSI Value')
    axs[0].set_ylabel('CSI proportion value')

    x = np.arange(0, len(magnitude_buffer), 1)
    axs[1].cla()
    axs[1].plot(x, magnitude_buffer)
    axs[1].set_title('Magnitudes')
    axs[1].set_xlabel('Index')
    axs[1].set_ylabel('Magnitude')

    x = np.arange(0, len(phase_buffer), 1)
    axs[2].cla()
    axs[2].plot(x, phase_buffer)
    axs[2].set_title('Phases')
    axs[2].set_xlabel('Index')
    axs[2].set_ylabel('Phase')

    plt.tight_layout()
    plt.pause(0.01)

# Main loop
try:
    while True:
        # Read raw CSI data from serial port
        try:
            line=ser.readline().decode().strip()
            print(line)
            if line.startswith("CSI_DATA"):
                # print(line)
                data_str = line.split(",")[-1]
                data_str = data_str[1:-1].strip().split(" ")
                # print(data_str)
                # raw_csi_data = [int(x) for x in data_str]
                raw_csi_data = [float(x)/128 for x in data_str]

                # Append raw CSI data to buffer
                raw_csi_buffer.extend(raw_csi_data)
                # Calculate magnitudes and phases
                magnitudes = raw_csi_to_magnitudes(raw_csi_data)
                phases = raw_csi_to_phases(raw_csi_data)
                # Append magnitudes and phases to buffers
                magnitude_buffer.extend(magnitudes)
                phase_buffer.extend(phases)
                # Update plots
                update_plot()
        except UnicodeDecodeError as e:
            print(e)
        except ValueError as e:
            print(e)
except KeyboardInterrupt:
    # Close serial port and exit
    ser.close()
    plt.close()
