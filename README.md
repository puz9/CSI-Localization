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
