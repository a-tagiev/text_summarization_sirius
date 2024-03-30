import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import Bots.Summary.BotWithServer.Helpers.bot_functions as bot
import Bots.Summary.BotWithServer.Helpers.functions as functions
from Bots.Summary.BotWithServer.Helpers.tokenBot import main_token, group_id
import Bots.Summary.BotWithServer.Helpers.bot_texts as bot_messages

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)
upload = vk_api.VkUpload(vk_session)

print("Bot started")


def handle_request(event):
    if '[club225246870|@club225246870] с а' == event.message['text'] or '[club225246870|VK Summary Bot] с а' == \
            event.message['text']:
        bot.check_lion_command(event, vk, upload)
        summary_command_abstract(event)
    elif '[club225246870|@club225246870] с э' == event.message['text'] or '[club225246870|VK Summary Bot] с э' == \
            event.message['text']:
        bot.check_lion_command(event, vk, upload)
        summary_command_extract(event)
    elif '[club225246870|@club225246870]' == event.message['text'] or '[club225246870|VK Summary Bot]' == event.message[
        'text']:
        bot.check_lion_command(event, vk, upload)
        bot.send_message(event.chat_id, bot_messages.help_message, vk=vk)
    elif '[club225246870|@club225246870] т' == event.message['text'] or '[club225246870|VK Summary Bot] т' == \
            event.message['text']:
        bot.check_lion_command(event, vk, upload)
        tonal_command(event)


def summary_command_extract(event):
    tagged_message = bot.find_tagged_message(event)  # ищем тегнутое сообщение
    if tagged_message:
        chat_id = event.chat_id
        start_message_id = tagged_message['date']  # беру айди тегнутого - стартового собщения
        messages = bot.get_message_history(chat_id, start_message_id, vk)  # беру все сообщения

        select_messages = ""
        select_messages_count = 0

        users = {}

        for message in messages[::-1]:
            if message['date'] >= start_message_id:
                if not functions.check_ai_marker(message['text']):
                    select_messages += message['text'] + "  "
                    select_messages_count += 1

        functions.process_request({"select_messages": select_messages,
                                   'select_messages_count': select_messages_count,
                                   'chat_id': chat_id}, "summarization_text_extract")
    else:
        bot.send_message(event.chat_id, bot_messages.zero_selected_message, vk=vk)


def summary_command_abstract(event):
    tagged_message = bot.find_tagged_message(event)  # ищем тегнутое сообщение
    if tagged_message:
        chat_id = event.chat_id
        start_message_id = tagged_message['date']  # беру айди тегнутого - стартового собщения
        messages = bot.get_message_history(chat_id, start_message_id, vk)  # беру все сообщения

        select_messages = ""
        select_messages_count = 0

        users = {}

        for message in messages[::-1]:
            if message['date'] >= start_message_id:
                if not functions.check_ai_marker(message['text']):
                    select_messages += message['text'] + "  "
                    select_messages_count += 1
                    # try:
                    #     user_id = message['from_id']
                    #     if user_id not in users:
                    #         user_info = vk.users.get(user_ids=user_id)
                    #         users[user_id] = {
                    #             'first_name': user_info[0]['first_name'],
                    #             'last_name': user_info[0]['last_name']}
                    #
                    #     user_data = users[user_id]
                    #     select_messages += f"<{user_data['first_name']} {user_data['last_name']}> {message['text']} \n"
                    #     select_messages_count += 1
                    # except:
                    #     pass
        functions.process_request({"select_messages": select_messages,
                                   'select_messages_count': select_messages_count,
                                   'chat_id': chat_id}, "summarization_text_abstract")
    else:
        bot.send_message(event.chat_id, bot_messages.zero_selected_message, vk=vk)


def tonal_command(event):
    tagged_message = bot.find_tagged_message(event)  # ищем тегнутое сообщение
    if tagged_message:
        functions.process_request({"tagged_message": tagged_message['text'],
                                   'chat_id': event.chat_id}, "tonal_text")
    else:
        bot.send_message(event.chat_id, bot_messages.zero_selected_message, vk=vk)


for start in longpoll.listen():
    if start.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if start.from_chat and start.message['from_id'] > 0:
            bot.send_message(start.chat_id, bot_messages.help_message, vk=vk)
            break

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if event.from_chat and event.message['from_id'] > 0:
            try:
                handle_request(event)
            except:
                pass
