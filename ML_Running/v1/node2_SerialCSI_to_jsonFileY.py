import serial
import json
import time
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT="COM16"


ser=serial.Serial(port=PORT,baudrate=921600,timeout=1)
json_file_name="csi_data_y.json"



start_time=time.time()
def get_time():
    return time.time()-start_time
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
                print("^^^Wrote to file^^^")
                with open(json_file_name,"w") as f:
                    json.dump(csi_data,f)
                last_write_to_file_time=get_time()
        else:
            print(line)
    except UnicodeDecodeError as e:
        print(e)
        continue
    except json.JSONDecodeError as e:
        print(e)
        continue
    except KeyboardInterrupt:
        ser.close()
        exit(0)