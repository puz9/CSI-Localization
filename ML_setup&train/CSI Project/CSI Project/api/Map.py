from pydantic import BaseModel
class MapData(BaseModel):
    variance: float
    skewness: float
    curtosis: float
    entropy: float