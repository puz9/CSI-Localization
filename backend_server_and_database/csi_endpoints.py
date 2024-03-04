import datetime
from fastapi import APIRouter, HTTPException
from typing import List

from pydantic import ValidationError
from CSIDataSchema import CSI_Data, CSI_DataXY, Time_And_CSI_Data
import pandas as pd
import json

path_csi_x_data="collected_datas/csi_datas_x.csv"
path_csi_y_data="collected_datas/csi_datas_y.csv"

csi_router = APIRouter()



@csi_router.post("/csi_data/{axis}/raw/upload")
def upload_raw_CSI_data_to_server(axis: str,request_body: CSI_Data):
    axis=axis.lower()
    path_csv=""
    if axis=="x":
        path_csv=path_csi_x_data
    elif axis=="y":
        path_csv=path_csi_y_data
    else:
        raise HTTPException(status_code=400, detail="Axis must be either x or y")
    df=pd.read_csv(path_csv)
    print(request_body.csi_data)
    new_data=pd.DataFrame({
        "timestamp":[datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "csi_data":[request_body.csi_data]
    },index=[0])
    df=pd.concat([df,new_data],ignore_index=True)
    df.to_csv(path_csv,index=False)
    return {"message": "CSI data uploaded"}
@csi_router.post("/csi_data_both_axis/raw/upload")
def upload_raw_CSI_data_to_server_both_axis(request_body : CSI_DataXY):
    print("fuck")
    df_x=pd.read_csv(path_csi_x_data)
    new_data=pd.DataFrame({
        "timestamp":[datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "csi_data":[request_body.csi_data_x]
    },index=[0])
    df_x=pd.concat([df_x,new_data],ignore_index=True)
    df_x.to_csv(path_csi_x_data,index=False)

    df_y=pd.read_csv(path_csi_y_data)
    new_data=pd.DataFrame({
        "timestamp":[datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "csi_data":[request_body.csi_data_y]
    },index=[0])
    df_y=pd.concat([df_y,new_data],ignore_index=True)
    df_y.to_csv(path_csi_y_data,index=False)
    return {"message": "CSI data uploaded"}



@csi_router.get("/csi_data/{axis}/raw/latest",response_model=Time_And_CSI_Data)
async def get_latest_raw_csi_data(axis:str):
    axis=axis.lower()
    path_csv=""
    if axis=="x":
        path_csv=path_csi_x_data
    elif axis=="y":
        path_csv=path_csi_y_data
    else:
        raise HTTPException(status_code=400, detail="Axis must be either x or y")
    df=pd.read_csv(path_csv)
    timestamp=df.iloc[-1]["timestamp"]
    csi_data=df.iloc[-1]["csi_data"]
    return Time_And_CSI_Data(
        timestamp=timestamp,
        csi_data=json.loads(csi_data)
    )
@csi_router.get("/csi_data/{axis}/magnitude/latest")
async def _():
    pass
@csi_router.get("/csi_data/{axis}/phase/latest")
async def _():
    pass

@csi_router.get("/csi_data/{axis}/raw/all",response_model=List[Time_And_CSI_Data])
async def get_all_raw_csi_data(axis:str):
    axis=axis.lower()
    path_csv=""
    if axis=="x":
        path_csv=path_csi_x_data
    elif axis=="y":
        path_csv=path_csi_y_data
    else:
        raise HTTPException(status_code=400, detail="Axis must be either x or y")
    df=pd.read_csv(path_csv)
    df["csi_data"]=df["csi_data"].map(json.loads)
    resp=[Time_And_CSI_Data(
        timestamp=timestamp,
        csi_data=csi_data
    ) for timestamp,csi_data in zip(df["timestamp"],df["csi_data"])]
    return resp
@csi_router.get("/csi_data/{axis}/magnitude/all")
async def _():
    pass
@csi_router.get("/csi_data/{axis}/phase/all")
async def _():
    pass