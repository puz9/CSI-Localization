from pydantic import BaseModel, Field, validator
import random

class CSI_Data(BaseModel):
    csi_data: list[int] = Field(...,example=[random.randint(-127,128) for i in range(93)])

class Time_And_CSI_Data(BaseModel):
    timestamp: str
    csi_data: list[int] = Field(...,example=[random.randint(-127,128) for i in range(93)])