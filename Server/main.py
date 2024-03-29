import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from Bots.Summary.Server.summarization_model import model
from Bots.Summary.Server.vk_bot_output import vk_bot
from Bots.Summary.Server.helpers.functions import make_perfect_answer


app = FastAPI()


class ResponseInput(BaseModel):
    select_messages: str
    select_messages_count: int
    chat_id: int


@app.get("/")
def home():
    return {"message": "OK"}


@app.post("/summarization_text")
def predict_status(response: ResponseInput):
    summary = model.summarize_text(response.select_messages)
    summary_message = make_perfect_answer(summary, response.select_messages_count)
    vk_bot.sender(response.chat_id, summary_message)


if __name__ == "__main__":
    uvicorn.run("main:app", port=11, host="90.156.135.118", reload=True)