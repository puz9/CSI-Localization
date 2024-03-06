from collections import Counter, deque
import math
import time
import joblib
import numpy as np
import requests
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))




# model=joblib.load('knn_model_v1.pkl')
model=joblib.load('mlp_model.pkl')

def set_of_csi_to_map_data():
    pass
def set_of_csi_to_cell_index():
    pass
def concat_and_flatten_pair_of_set_of_csi(csi_datas_x,csi_datas_y):#might be good for still object
    csi_datas_x=np.array([np.array(csi) for csi in csi_datas_x])
    csi_datas_y=np.array([np.array(csi) for csi in csi_datas_y])

    a=np.array([csi_datas_x,csi_datas_y])
    features=a.reshape(-1)/128
    # print(type(features[0]))
    # features=np.concatenate(a,axis=0)
    return features
def sd_on_pair_of_set_csi_then_concat_and_flatten(csi_datas_x,csi_datas_y):#might be good for moving object
    if len(csi_datas_x)!=len(csi_datas_y):
        return ValueError(f"len(csi_datas_x)!=len(csi_datas_y) ; {len(csi_datas_x)}!={len(csi_datas_y)}")
    #mean of columns for both csi
    mean_of_columns_x=np.mean(csi_datas_x, axis=0)
    mean_of_columns_y=np.mean(csi_datas_y, axis=0)

    row_sampling_range=20 #not used
    rows_amount=min(len(csi_datas_x),len(csi_datas_y)) #likely equal
    transformed_x=[[0 for __ in range(128)] for _ in range(rows_amount-row_sampling_range)]
    transformed_y=[[0 for __ in range(128)] for _ in range(rows_amount-row_sampling_range)]
    
    for row_index in range(rows_amount):
        for column_index in range(128):
            new_val_x=0
            new_val_y=0
            for row_index_sub in range(row_index,row_index+row_sampling_range):
                new_val_x+=(csi_datas_x[row_index_sub][column_index]-mean_of_columns_x[column_index])**2
                new_val_y+=(csi_datas_y[row_index_sub][column_index]-mean_of_columns_y[column_index])**2
            new_val_x/=row_sampling_range
            new_val_y/=row_sampling_range
            new_val_x=math.sqrt(new_val_x)
            new_val_y=math.sqrt(new_val_y)
            transformed_x[row_index][column_index]=new_val_x
            transformed_y[row_index][column_index]=new_val_y
    features=np.array([transformed_x,transformed_y])
    # features=np.array(r).reshape(2,-1)
    features=features.reshape(-1)
    return features
def pair_of_set_of_csi_to_features(csi_datas_x,csi_datas_y):
    # return sd_on_pair_of_set_csi_then_concat_and_flatten(csi_datas_x,csi_datas_y)
    return concat_and_flatten_pair_of_set_of_csi(csi_datas_x,csi_datas_y)

def get_one_human_cell_index(csi_datas_x:np.array,csi_datas_y:np.array) -> int:
    global model
    if csi_datas_x.shape[0]!=20 or csi_datas_x.shape[1]!=128:
        raise ValueError("csi_datas_x.shape[0]!=20 or csi_datas_x.shape[1]!=128")
    if csi_datas_y.shape[0]!=20 or csi_datas_y.shape[1]!=128:
        raise ValueError("csi_datas_y.shape[0]!=20 or csi_datas_y.shape[1]!=128")
    
    features=pair_of_set_of_csi_to_features(csi_datas_x,csi_datas_y)
    if len(features)==0:
        return
    return model.predict([features])[0]
    
answers=deque(maxlen=10)
def get_map_data(csi_datas_x : list[int],csi_datas_y : list[int]) -> list[list[int]]:
    global answers
    next_cell_index=get_one_human_cell_index(csi_datas_x,csi_datas_y)
    answers.append(next_cell_index)
    
    cell_index=Counter(answers).most_common(1)[0][0]

    map_r=[
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
    if cell_index==0:
        return map_r
    cell_index-=1
    map_r[cell_index//4][cell_index%4]=1
    return map_r



while True:
    try:
        with open("csi_datas_x.json","r") as f:
            csi_datas_x=np.array(json.load(f))
        with open("csi_datas_y.json","r") as f:
            csi_datas_y=np.array(json.load(f))
        map_data=get_map_data(csi_datas_x,csi_datas_y)
        for row in map_data:
            print(row)
        
        resp=requests.post(
            "http://localhost:8000/map_data/upload",
            json={
                "map_data":map_data
            }
        )
        print(resp.text)
    except requests.exceptions.ConnectionError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(e)
    except ConnectionError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    time.sleep(0.01)