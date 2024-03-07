from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from loguru import logger

from app.model import predict_pipeline
from app.preprocess.preprocessing  import preprocessing

cache = {}

app = FastAPI()

class TextIn(BaseModel):
    review: str

class PredictionOut(BaseModel):
    sentiment: str

@app.get('/')
async def home():
    return {'text': "Nguyen's Thesis"}

@app.post("/predict", response_model=PredictionOut)
async def predict(payload: TextIn):

    if payload.review != '':
        review_handled = preprocessing(payload.review)
        sentiment = predict_pipeline(review_handled)
        return {"sentiment": sentiment}

    return {"error": "Please try again!"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=30000)