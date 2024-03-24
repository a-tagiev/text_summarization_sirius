from model import model
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class TextInput(BaseModel):
    text: str


class PredictOutput(BaseModel):
    predict: str


@app.get("/")
def home():
    return {"message": "OK"}


@app.post("/predict", response_model=PredictOutput)
def predict_status(input: TextInput):
    status = model.predict_pipeline(input.text)
    return {"predict": status}