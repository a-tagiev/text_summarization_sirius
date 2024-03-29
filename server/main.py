import uvicorn

from models import tonality_model
from fastapi import FastAPI
from pydantic import BaseModel
from vk_bot_output import vk_bot


app = FastAPI()


class TextInput(BaseModel):
    text: str
    chat_id: int


@app.get("/")
def home():
    return {"message": "OK"}


@app.post("/text_tonality")
async def predict_status(input: TextInput):
    predict_tonality = tonality_model.model.tonality_predict(input.text)
    vk_bot.sender(input.chat_id, predict_tonality["label"].lower())


if __name__ == "__main__":
    uvicorn.run("main:app", port=80, host="0.0.0.0", reload=True)