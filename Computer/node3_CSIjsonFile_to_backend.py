import time
import requests
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

while True:
    try:
        with open("csi_data_x.json","r") as f:
            csi_data_x=json.load(f)
        with open("csi_data_y.json","r") as f:
            csi_data_y=json.load(f)
        resp=requests.post(
            "http://localhost:8000/csi_data_both_axis/raw/upload",
            json={
                "csi_data_x":csi_data_x,
                "csi_data_y":csi_data_y
            }
        )
        print(resp.text)
    except ConnectionError as e:
        print(e)
    time.sleep(1)