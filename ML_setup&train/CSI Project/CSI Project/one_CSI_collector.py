import csv
import serial
import time

ser=serial.Serial('COM8', 921600)
ser.flushInput()
ser.flushOutput()

with open('csi_data.csv', 'w', newline='\n') as file:
    writer = csv.writer(file)
    line="type,role,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,real_time_set,real_timestamp,len,CSI_DATA"
    writer.writerow(line.split(","))

while True:
    try:
        line=ser.readline()
        line = line.decode('utf-8').strip()
        print(line)
        if line.startswith("type,"):
            with open('csi_data.csv', 'w', newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow(line.split(","))
        if line.startswith("CSI_DATA"):
            print(line)
            with open('csi_data.csv', 'a', newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow(line.split(","))
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        continue
ser.close()