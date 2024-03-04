from pydantic import BaseModel, Field, validator
import random

class CSI_Data(BaseModel):
    csi_data: list[int] = Field(...,example=[random.randint(-127,128) for i in range(128)])

class Time_And_CSI_Data(BaseModel):
    timestamp: str
    csi_data: list[int] = Field(...,example=[random.randint(-127,128) for i in range(128)])

class CSI_DataXY(BaseModel):
    csi_data_x: list[int] = Field(...,example=[random.randint(-127,128) for i in range(128)])
    csi_data_y: list[int] = Field(...,example=[random.randint(-127,128) for i in range(128)])