import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from helpers.token_bot import main_token, group_id
from helpers.functions import *
from helpers.bot_functions import find_tagged_message

#
# vk_session = vk_api.VkApi(token=main_token)
# vk = vk_session.get_api()
# longpoll = VkBotLongPoll(vk_session, group_id)
#
#
# def send_request_to_fastapi(data):
#     response = requests.post(f"{FastApi_URL}/text tonality", json=data)
#     return response.json()
#
#
# print("Start")
# for event in longpoll.listen():
#     if event.type == VkBotEventType.MESSAGE_NEW:
#         if event.from_chat:
#             message_text = event.object['message']['text'].lower()
#             peer_id = event.object['message']['peer_id']
#             print("working with " + message_text)
#
#             action = "simple message"
#             try:
#                 action = event.message['action']['type']
#             except:
#                 pass
#
#             if action == "simple message":
#                 server_response = send_request_to_fastapi({"text": message_text})
#                 print(server_response["predict"])
#                 sender(peer_id=peer_id, message=server_response["predict"])




vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)


def handle_request(event):
    if '/summary' in event.message['text']:
        summary_command(event)
    if '/help' in event.message['text']:
        help_command(event)


def help_command(event):
    print("help")


def summary_command(event):
    tagged_message = find_tagged_message(event)  # ищем тегнутое сообщение
    if tagged_message:
        chat_id = event.chat_id
        start_message_id = tagged_message['date']  # беру айди тегнутого - стартового собщения
        messages = bot.get_message_history(chat_id, start_message_id, vk)  # беру все сообщения

        for message in messages[::-1]:  # перебираю все сообщения чата :(
            if message['date'] >= start_message_id:  # только сообщения, которые поступили после тегнутого
                if not functions.check_ai_marker(message['text']):
                    select_messages += message['text'] + " "  # пополняю текст для суммаризации
                    select_messages_count += 1

        bot.process_request({"select_messages": select_messages,
                             'select_messages_count': select_messages_count,
                             'chat_id': chat_id})



for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if event.from_chat and event.message['from_id'] > 0:
            handle_request(event)
