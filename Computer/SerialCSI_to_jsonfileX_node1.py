import serial
import json
import time


start_time=time.time()
def get_time():
    return time.time()-start_time

ser=serial.Serial(port="COM3",baudrate=115200,timeout=1)
json_file_name="csi_data_x.json"


last_write_to_file_time=get_time()
interval_write_file=1


while True:
    try:
        line=ser.readline().decode("utf-8").strip()
        # print(line)
        if line.startswith("CSI_DATA"):
            csi_data=line.split(",")[-1][1:-1].strip().split(" ")
            csi_data=[int(i) for i in csi_data]
            if len(csi_data)!=128:
                print("Invalid data")
                continue
            print(csi_data)

            if(get_time()-last_write_to_file_time>=interval_write_file):
                print("^^^Write to file^^^")
                with open(json_file_name,"w") as f:
                    json.dump(csi_data,f)
                last_write_to_file_time=get_time()
        else:
            print(line)
    except UnicodeEncodeError as e:
        print(e)
        continue
    except json.JSONDecodeError as e:
        print(e)
        continue