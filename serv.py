# import random
#
# import uvicorn
# from Bots.Summary.Helpers.functions import make_perfect_answer
# from Bots.Summary.Model.model import summarize_text
# from fastapi import FastAPI, Response
# from pydantic import BaseModel
#
#
# print("start")
# app = FastAPI()
# uvicorn.run("serv:app", port=81, host="0.0.0.0", reload=True)
#
#
#
# class ResponseInput(BaseModel):
#     select_messages: str
#     select_messages_count: int
#     chat_id: str
#
#
# @app.post("/predict")
# async def predict_status(response: ResponseInput):
#     out_summary = summarize_text(response.select_messages)
#     out_message = make_perfect_answer(out_summary, response.select_messages_count)
#     send_message(chat_id=response.chat_id, message=out_message)
#     return Response(status_code=200)
#
#
# # def send_message(chat_id, message):
# #     vk.messages.send(
# #         random_id=random.randint(1, 100000),
# #         chat_id=chat_id,
# #         message=str(message)
# #     )
#
#
# if __name__ == "__main__":
#     uvicorn.run("serv:app", port=81, host="0.0.0.0", reload=True)
#
#
# from Bots.Summary.bot import send_message
