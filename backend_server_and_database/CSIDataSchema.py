from pydantic import BaseModel, Field, validator
import random

class CSI_Data(BaseModel):
    csi: list[int] = Field(...,example=[random.randint(-128,128) for i in range(93)])

class Time_And_CSI_Data(BaseModel):
    timestamp: str
    csi: list[int] = Field(...,example=[random.randint(-128,128) for i in range(93)])