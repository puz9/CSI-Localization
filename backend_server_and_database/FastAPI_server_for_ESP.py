from fastapi import FastAPI
import json
import os
from collections import deque
import time
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import pandas as pd
from datetime import datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))



app = FastAPI()

origins = [
    "http://localhost:5173",
    # Add more allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/upload_map_data")
def save_map_data(data: dict):
    
    df=pd.read_csv("map_datas.csv")

    new_data=pd.DataFrame({
        "timestamp":[datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "map":[json.dumps(data["map"])]
    },index=[0])
    df=pd.concat([df,new_data],ignore_index=True)
    
    df.to_csv("map_datas.csv",index=False)
    return {"message": "Map data uploaded"}



@app.get("/get_map_data")
def return_map_data():
    # import json
    # import requests
    
    # json_data = requests.get('https://4fbc-2405-9800-b671-2af7-54ba-c2b0-542f-1287.ngrok-free.app/get_data').text
    
    # data_dict = json.loads(json_data)

    # latest_data=data_dict["data"][-1]
    # map_data_return=latest_data["Data"]
    # return {"map": map_data_return}
    df=pd.read_csv("map_datas.csv")
    map_data=df.iloc[-1]["map"]
    return {"map": json.loads(map_data)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)