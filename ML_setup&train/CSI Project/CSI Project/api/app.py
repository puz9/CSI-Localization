# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from tensorflow import keras

app = FastAPI()
model = keras.models.load_model('trained_model.h5')

# Define the input data model
class InputData(BaseModel):
    feature1: float
    feature2: float

# Load the trained model
model = joblib.load("model.pkl")

# Define prediction function
def predict(features):
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)
    return prediction[0]

# Define API endpoint for making predictions
@app.post("/predict")
async def make_prediction(data: InputData):
    features = [data.feature1, data.feature2]
    prediction = predict(features)
    return {"prediction": prediction}
