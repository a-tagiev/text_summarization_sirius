import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from app.model import model

from tokenBot import main_token, group_id

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
long_poll = VkLongPoll(vk_session)


def sender(text, id):
    vk.messages.send(user_id=id, message=text, random_id=0)


print("Start")
for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.from_user:
            msg = event.message
            print("working with " + msg)
            predict = model.predict_pipeline(msg)
            print(predict[0])
            sender(id=event.user_id, text=predict[0]["label"])





# vk = vk_api.VkApi(token=main_token)
# vk._auth_token()
# vk.get_api()
# longpoll = VkBotLongPoll(vk, group_id)
#
#
# def send_msg(peer_id: int, message: str, attachment: str = ""):
#     return vk.method("messages.send", {**locals(), "random_id": 0})
#
#
# while True:
#     try:
#         for event in longpoll.listen():
#             if event.type == VkBotEventType.MESSAGE_NEW:
#                 if event.from_user:
#                     msg = event.message
#                     predict = model.predict_pipeline(msg)
#
#                     send_msg(peer_id=event.obj.peer_id, message=predict["label"])
#     except Exception as e:
#         print(repr(e))
