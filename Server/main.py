import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from Bots.Summary.Server.summarization_model import model
from Bots.Summary.Server.vk_bot_output import vk_bot
from Bots.Summary.Server.helpers.functions import make_perfect_answer

app = FastAPI()


class SummaryInput(BaseModel):
    select_messages: str
    select_messages_count: int
    chat_id: int


class TonalInput(BaseModel):
    tagged_message: str
    chat_id: int


@app.get("/")
def home():
    return {"message": "OK"}


@app.post("/summarization_text_extract")
def predict_status(response: SummaryInput):
    summary = model.summarize_text_extract(response.select_messages)
    summary_message = make_perfect_answer(summary, response.select_messages_count)
    vk_bot.sender(response.chat_id, summary_message)


@app.post("/summarization_text_abstract")
def predict_status(response: SummaryInput):
    summary = model.summarize_text_abstract(response.select_messages)
    summary_message = make_perfect_answer(summary, response.select_messages_count)
    vk_bot.sender(response.chat_id, summary_message)


@app.post("/tonal_text")
def predict_status(response: TonalInput):
    total = model.tonality_predict(response.tagged_message)
    vk_bot.sender(response.chat_id, total)


if __name__ == "__main__":
    uvicorn.run("main:app", port=11, host="0.0.0.0", reload=True)