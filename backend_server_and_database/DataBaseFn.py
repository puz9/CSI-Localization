import pandas as pd
import json

path_csi_x_data="collected_datas/csi_datas_x.csv"
path_csi_y_data="collected_datas/csi_datas_y.csv"
path_map_data="collected_datas/map_datas.csv"

def insert_csi_data(csi_data,axis):
    axis=axis.lower()
    path=""
    if axis=="x":
        path=path_csi_x_data
    elif axis=="y":
        path=path_csi_y_data
    else:
        raise ValueError("Axis must be either x or y")
    df=pd.read_csv(path)
    new_data=pd.DataFrame({
        "timestamp":[csi_data.timestamp],
        "csi":[json.dumps(csi_data.csi)]
    },index=[0])
    df=pd.concat([df,new_data],ignore_index=True)
    df.to_csv(path,index=False)