# CSI-Localization

My IP address is in here. Feel free to hack me.

run script script `backend_server_and_database/main_FastAPI_server.py`

## Backend

```
pip install -r requirements.txt or pip3 install -r requirements.txt
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
python ML_Running/node1_SerialCSI_to_jsonFileX.py

#Terminal 2
python ML_Running/node2_SerialCSI_to_jsonFileY.py

#Terminal 3
python ML_Running/node3_CSIjsonFile_to_backend.py

#Terminal 4
python ML_Running/node4_CSIjsonFile_to_map_to_backend.py
```
