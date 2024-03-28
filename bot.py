import vk_api
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import Bots.Summary.Helpers.bot_functions as bot
import Bots.Summary.Helpers.functions as functions
from Bots.Summary.Helpers.tokenBot import main_token, group_id, FastApi_URL



vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)



print("Bot started")


def send_message(chat_id, message):
    vk.messages.send(
        random_id=random.randint(1, 100000),
        chat_id=chat_id,
        message=str(message)
    )


def handle_request(event):
    if '/summary' in event.message['text']:
        summary_command(event)
    if '/help' in event.message['text']:
        help_command(event)


def summary_command(event):
    tagged_message = bot.find_tagged_message(event)  # ищем тегнутое сообщение
    if tagged_message:
        chat_id = event.chat_id
        start_message_id = tagged_message['date']  # беру айди тегнутого - стартового собщения
        messages = bot.get_message_history(chat_id, start_message_id, vk)  # беру все сообщения

        select_messages = ""
        select_messages_count = 0

        for message in messages[::-1]:  # перебираю все сообщения чата :(
            if message['date'] >= start_message_id:  # только сообщения, которые поступили после тегнутого
                if not functions.check_ai_marker(message['text']):
                    select_messages += message['text'] + " "  # пополняю текст для суммаризации
                    select_messages_count += 1

        bot.process_request({"select_messages": select_messages,
                             'select_messages_count': select_messages_count,
                             'chat_id': chat_id})


def help_command(event):
    print("help")


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if event.from_chat and event.message['from_id'] > 0:
            handle_request(event)
