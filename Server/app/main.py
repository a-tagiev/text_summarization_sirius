import socket
import time

from fastapi import FastAPI
from pydantic import BaseModel
from summarization_model import model
from Server.vk_bot_output import vk_bot
from helpers.functions import make_perfect_answer

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
    # for testing
    # time.sleep(10)
    return {"message": socket.gethostname()}


@app.post("/summarization_text_extract")
def predict_status(response: SummaryInput):
    # for testing
    # time.sleep(50)
    # print(response.select_messages)
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
    # for testing
    # time.sleep(50)
    # print(response.tagged_message)
    total = model.tonality_predict(response.tagged_message)
    vk_bot.sender(response.chat_id, total)

#
# if __name__ == "__main__":
#     uvicorn.run("main:app", port=11, host="90.156.135.118", reload=True)
