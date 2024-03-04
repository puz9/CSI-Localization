from fastapi import FastAPI
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from map_endpoints import map_router
from csi_endpoints import csi_router




app = FastAPI()

origins = [
    "http://localhost:5173",
    # Add more allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(map_router)
app.include_router(csi_router)
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)
    uvicorn.run("main_FastAPI_server:app", host="0.0.0.0", port=8000,reload=True)