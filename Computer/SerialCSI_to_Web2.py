import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from function_holder import *
import threading
import time
import requests
import random #for mock



def upload_map_data_thread():
    while True:
        try:
            csi_data_x=[random.randint(-127,128) for i in range(128)]
            csi_data_y=[random.randint(-127,128) for i in range(128)]
            map_data=get_map_data(csi_data_x,csi_data_y)
            print(map_data)
            # resp=requests.post("http://localhost:8000/map_data/upload",json={"map_data":map_data})
            # print(resp.text)
        except ConnectionError as e:
            print(e)
        time.sleep(1)


if __name__=="__main__":
    try:
        t3=threading.Thread(target=upload_map_data_thread)
        t3.start()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        exit(0)