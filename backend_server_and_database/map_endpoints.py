import datetime
from fastapi import APIRouter, HTTPException
from typing import List
from MapDataSchema import Map_Data, Time_And_Map_Data
import pandas as pd
import json

map_router=APIRouter()

path_map_data="collected_datas/map_datas.csv"



@map_router.post("/map_data/upload")
async def upload_latest_map_data_to_storage(map_data:Map_Data):
    try:
        validated_map_data = Map_Data(map_data=map_data.map_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    df=pd.read_csv(path_map_data)
    new_data=pd.DataFrame({
        "timestamp":[datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "map_data":[json.dumps(validated_map_data.map_data)]
    },index=[0])
    df=pd.concat([df,new_data],ignore_index=True)
    df.to_csv(path_map_data,index=False)
    return {"message": "Map data uploaded"}

@map_router.get("/map_data/all",response_model=List[Time_And_Map_Data])
async def obtain_all_map_data():
    df=pd.read_csv(path_map_data)
    df["map_data"]=df["map_data"].map_routerly(json.loads)

    resp=[Time_And_Map_Data(
        timestamp=timestamp,
        map_data=map_data
    ) for timestamp,map_data in zip(df["timestamp"],df["map_data"])]
    return resp

@map_router.get("/map_data/latest",response_model=Time_And_Map_Data)
async def obtain_latest_map_data():
    df=pd.read_csv(path_map_data)
    timestamp=df.iloc[-1]["timestamp"]
    map_data=df.iloc[-1]["map_data"]
    return Time_And_Map_Data(
        timestamp=timestamp,
        map_data=json.loads(map_data)
    )