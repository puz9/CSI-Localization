from collections import Counter, deque
import math
import joblib
import os

model=joblib.load('knn_model.pkl')

def normalize_raw_csi(raw_csi):
    return [v/128 for v in raw_csi]

def raw_csi_to_magnitudes(raw_csi):
    magnitudes = []
    if len(raw_csi)!=128:
        raise ValueError("CSI data must be 128 in length")
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
    if len(raw_csi)!=128:
        raise ValueError("CSI data must be 128 in length")
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
    rx=raw_csi_to_magnitudes(csi_data_x)
    if len(rx)==0:
        print("Not enough data from X axis")
        return []
    ry=raw_csi_to_magnitudes(csi_data_y)
    if len(ry)==0:
        print("Not enough data from Y axis")
        return []
    # rx=normalize_magnitudes(rx)
    # ry=normalize_magnitudes(ry)
    features=rx+ry
    return features

def get_one_human_cell_index(csi_data_x,csi_data_y):
    global model
    features=raw_csi_to_features(csi_data_x,csi_data_y)
    if len(features)==0:
        return
    return model.predict([features])[0]
    
answers=deque(maxlen=10)
def get_map_data(csi_data_x,csi_data_y):
    global answers
    next_cell_index=get_one_human_cell_index(csi_data_x,csi_data_y)
    answers.append(next_cell_index)
    
    cell_index=Counter(answers).most_common(1)[0][0]

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

