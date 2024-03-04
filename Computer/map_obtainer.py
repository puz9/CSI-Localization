#Obtain the map from the result of the model then save as file
#Possibly upload to backend too.

import json
import tensorflow as tf
import keras
import os
import random

#cd to the directory of the file
os.chdir(os.path.dirname(os.path.abspath(__file__)))



map_data=[
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

def obtain_map():
    #Obtain the map using result from keras stuff
    global map_data

    #...Should be the code to use the weight and model
    map_data=[
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,1,0]
    ]
    for i in range(4):
        for j in range(4):
            map_data[i][j]=random.randint(0,1)

obtain_map()


data={
    "map": map_data,
}
f=open("data.json","w")
f.write(json.dumps(data,indent=4))
f.close()