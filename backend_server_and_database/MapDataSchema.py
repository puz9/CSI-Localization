from pydantic import BaseModel, Field, validator
import random

class Map_Data(BaseModel):
    map_data:list[list[int]] = Field(...,example=[
        [0,1,0,0],
        [0,1,0,0],
        [0,0,1,1],
        [0,0,0,0]
    ])
    @validator("map_data")
    def check_map_size(cls, v):
        if len(v) != 4 or any(len(row) != 4 for row in v):
            raise ValueError("Map data must be a 4x4 array.")
        return v
class Time_And_Map_Data(BaseModel):
    timestamp:str = Field(...,example="2024-03-03 21:39:22")
    map_data:list[list[int]] = Field(...,example=[
        [0,1,0,0],
        [0,1,0,0],
        [0,0,1,1],
        [0,0,0,0]
    ])

