from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message": "Hello World"}

@app.get("/map/{x}")
async def root(x):
    types = x.split(',')
    return {
        "map": [[int(types[0]),int(types[1]),int(types[2]),int(types[3])],
                [int(types[4]),int(types[5]),int(types[6]),int(types[7])],
                [int(types[8]),int(types[9]),int(types[10]),int(types[11])],
                [int(types[12]),int(types[13]),int(types[14]),int(types[15])]
            ]  
        }
   