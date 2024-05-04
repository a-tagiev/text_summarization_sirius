import os
import pika
import vk_api
from pydantic import BaseModel
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import Helpers.bot_functions as bot
import Helpers.functions as functions
from Helpers.tokenBot import main_token, group_id
import Helpers.bot_texts as bot_messages


EXCHANGE_NAME = "input_exchange"


def handle_request(event):
    if '[club225246870|@club225246870] с' == event.message['text'] or '[club225246870|VK Summary Bot] с' == \
            event.message['text']:
        summary_command(event)
    elif '[club225246870|@club225246870]' == event.message['text'] or '[club225246870|VK Summary Bot]' == event.message[
        'text']:
        bot.send_message(event.chat_id, bot_messages.help_message, vk=vk)


def summary_command(event):
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
                if not functions.check_ai_marker(message['text']):  # смотрим что сообщение не техническое
                    select_messages += message['text'] + " , "
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
                    #     select_messages += "error"
                    #     select_messages_count += 1

        functions.process_request({"select_messages": select_messages,
                                   'select_messages_count': select_messages_count,
                                   'chat_id': chat_id,
                                   'flag_output': 'vk_bot'}, channel)
    else:  # инвалидное сообщение отылаем
        bot.send_message(event.chat_id, bot_messages.zero_selected_message, vk=vk)


if __name__ == '__main__':

    print("Bot started")

    vk_session = vk_api.VkApi(token=main_token)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)

    amqp_url = os.environ['AMQP_URL']
    url_params = pika.URLParameters(amqp_url)
    url_params.heartbeat = 0

    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            # Проверяем, что сообщение отправлено не ботом
            if event.from_chat and event.message['from_id'] > 0:
                try:
                    handle_request(event)
                except Exception as e:
                    print(f"An error occurred: {e}")

    connection.close()


