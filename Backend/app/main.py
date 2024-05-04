import socket
import time
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from summary_model import model
import uvicorn

from producer import send_to_rabbitmq

app = FastAPI()

class SummaryInput(BaseModel):
    select_messages: str
    flag_output: str
    chat_id: int
    select_messages_count: int


class SummaryOutput(BaseModel):
    text_summary: str
    chat_id: int
    select_messages_count: int





@app.get("/")
def home():
    # for testing
    time.sleep(10)
    # return {"message": socket.gethostname()}


@app.post("/summarization_text_extract")
def predict_status(response: SummaryInput):
    # for testing


    text = ' '.join(model.summarize(response.select_messages))

    data = SummaryOutput(text_summary=text, chat_id=response.chat_id, select_messages_count=response.select_messages_count)

    print(text)
    send_to_rabbitmq(data, response.flag_output)



    # summary = model.summarize_text_extract(response.select_messages)
    # summary_message = make_perfect_answer(summary, response.select_messages_count)
    # vk_bot.sender(response.chat_id, summary_message)


# @app.post("/summarization_text_abstract")
# def predict_status(response: SummaryInput):
#     summary = model.summarize_text_abstract(response.select_messages)
#     summary_message = make_perfect_answer(summary, response.select_messages_count)
#     vk_bot.sender(response.chat_id, summary_message)


# @app.post("/tonal_text")
# def predict_status(response: TonalInput):
#     # for testing
#     time.sleep(50)
#     print(response.tagged_message)
#     # total = model.tonality_predict(response.tagged_message)
#     # vk_bot.sender(response.chat_id, total)

