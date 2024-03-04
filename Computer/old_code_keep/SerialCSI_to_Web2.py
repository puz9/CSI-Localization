import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from Computer.old_code_keep.function_holder_CSI_analyzer import *
from Computer.old_code_keep.function_holder_CSI_obtainer import *
import threading
import time
import requests
import random #for mock



def upload_map_data_thread():
    while True:
        try:
            # csi_data_x=[random.randint(-127,128) for i in range(128)]
            # csi_data_x="110 96 6 0 0 0 0 0 0 0 0 0 1 -23 2 -20 1 -22 4 -22 5 -19 5 -19 7 -19 7 -18 8 -18 7 -16 8 -17 7 -16 8 -17 7 -14 7 -12 6 -15 6 -11 5 -10 4 -12 4 -11 3 -11 2 -11 4 -10 1 -12 3 -13 1 -11 0 0 0 -15 -2 -14 0 -12 -1 -11 -1 -12 -3 -14 -1 -16 -2 -15 -2 -15 -5 -11 -3 -15 -2 -13 -5 -13 -3 -11 -3 -13 -4 -13 -7 -15 -2 -9 -5 -11 -6 -11 -7 -9 -6 -10 -6 -8 -8 -6 -9 -8 -7 -4 0 0 0 0 0 0 0 0 0 0".split()
            # csi_data_x=[int(i) for i in csi_data_x]
            # csi_data_y="110 96 6 0 0 0 0 0 0 0 0 0 -19 6 -21 7 -20 6 -23 9 -23 6 -25 5 -23 7 -24 8 -26 5 -24 6 -27 6 -27 6 -27 5 -28 5 -28 3 -27 3 -25 4 -21 1 -25 3 -23 3 -23 2 -21 0 -19 0 -20 3 -20 3 -16 4 0 0 -15 4 -13 3 -16 6 -10 6 -14 3 -14 6 -11 4 -8 5 -8 5 -5 4 -7 6 -5 2 -5 5 -6 3 -2 5 -2 3 -1 3 0 3 3 2 3 2 4 1 2 1 4 1 7 0 5 1 6 1 0 0 0 0 0 0 0 0 0 0".split()
            # csi_data_y=[int(i) for i in csi_data_y]
            # print(len(csi_data_y))
            # csi_data_y=[random.randint(-127,128) for i in range(128)]
            # map_data=get_map_data(csi_data_x,csi_data_y)

            map_data=get_map_data(
                get_csi_data_x(),
                get_csi_data_y()
            )
            print(map_data)
            # resp=requests.post("http://localhost:8000/map_data/upload",json={"map_data":map_data})
            # print(resp.text)
        except ConnectionError as e:
            print(e)
        time.sleep(1)


if __name__=="__main__":
    try:
        start_CSI_obtainer()
        start_CSI_uploader()
        start_map_uploader()

        t3=threading.Thread(target=upload_map_data_thread)
        t3.start()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        exit(0)