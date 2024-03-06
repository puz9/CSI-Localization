# CSI-Localization

My IP address is in here. Feel free to hack me.

## Backend

```
pip install -r requirements.txt
python backend_server_and_database/main_FastAPI_server.py

```

## Frontend

```
cd frontend_webpage/frontend-react
npm i
npm run dev

```

## ML (Running)

```
#Terminal 1
python ML_Running/v2/node1_SerialCSI_to_jsonFileX.py

#Terminal 2
python ML_Running/v2/node2_SerialCSI_to_jsonFileY.py

#Terminal 3
python ML_Running/v2/node3_CSIjsonFile_to_map_to_backend.py
```


# Simple Data Collection
There are the scripts in `ML_setup&train\CSI Project`

`data_collect_x.py` and `data_collector_y.py`

paste these scripts in active_ap folder of esp32-csi-tool

This script will read serial. So you can verify esp32 that sends csi data properly and consistently

Press `B` to start data collection and Press `C` to stop data collection and save to csv.

# สมาชิก
1.นาย ญาโณทัย ไชยธวัช 6410500211

2.นาย พีรณัฐ ตรีวิภานนท์ 6410500289

3.นาย วรกร คุณวุฒิฤทธิรณ 6410501102

4.นาย กรพล กุลกรินีธรรม 6410501072

5.นาย ชวัลวิทย์ จอมวรวงศ์ 6410501081

6.นาย ญาณกร บรรจงวัฒน์ธนา 6410504071