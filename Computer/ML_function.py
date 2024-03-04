import math

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
    rx=raw_csi_to_magnitudes(csi_data_x)
    ry=raw_csi_to_magnitudes(csi_data_y)
    # rx=normalize_magnitudes(rx)
    # ry=normalize_magnitudes(ry)
    features=rx+ry
    return features


    