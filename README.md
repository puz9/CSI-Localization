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
