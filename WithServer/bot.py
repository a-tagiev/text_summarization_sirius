import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import Bots.Summary.WithServer.Helpers.bot_functions as bot
import Bots.Summary.WithServer.Helpers.functions as functions
from Bots.Summary.WithServer.Helpers.tokenBot import main_token, group_id
import Bots.Summary.WithServer.Helpers.bot_texts as bot_messages

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)

print("Bot started")


def handle_request(event):
    if '[club225246870|@club225246870] с' == event.message['text']:
        summary_command(event)
    if '[club225246870|@club225246870]' == event.message['text']:
        bot.send_message(event.chat_id, bot_messages.help_message, vk=vk)


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

        functions.process_request({"select_messages": select_messages,
                                   'select_messages_count': select_messages_count,
                                   'chat_id': chat_id})
    else:
        bot.send_message(event.chat_id, bot_messages.zero_selected_message, vk=vk)


for start in longpoll.listen():
    if start.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if start.from_chat and start.message['from_id'] > 0:
            bot.send_message(start.chat_id, bot_messages.start_message, vk=vk)
            break

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if event.from_chat and event.message['from_id'] > 0:
            handle_request(event)
