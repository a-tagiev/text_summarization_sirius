import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from tokenBot import main_token, FastApi_URL, group_id


vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)


def sender(peer_id, message):
    vk.messages.send(peer_id=peer_id, message=message, random_id=0)


def send_request_to_fastapi(data):
    response = requests.post(f"{FastApi_URL}/predict", json=data)
    return response.json()


print("Start")
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        message_text = event.object['message']['text'].lower()
        peer_id = event.object['message']['peer_id']
        print("working with " + message_text)
        server_response = send_request_to_fastapi({"text": message_text})
        print(server_response["predict"])
        sender(peer_id=peer_id, message=server_response["predict"])


