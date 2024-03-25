import uvicorn

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
async def predict_status(input: TextInput):
    status = model.predict_pipeline(input.text)
    return {"predict": status[0]["label"]}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)