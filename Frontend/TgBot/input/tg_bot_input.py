import asyncio
import logging
from db.db import chat_db
from aiogram import Bot, Dispatcher, types
import json
import os
import pika

from token_bot import TOKEN

EXCHANGE_NAME = "input_exchange"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    logging.info(f"Receiving message from chat {message.chat.id}: {message.text}, message_id: {message.message_id}")
    chat_db.insert_message(message.chat.id, message.message_id, message.from_user.id, message.text)
    if f'@{(await bot.me).username.lower()}' in message.text.lower():
        if message.reply_to_message:
            select_messages_count = message.message_id - message.reply_to_message.message_id + 1
            select_messages = chat_db.get_last_messages(message.chat.id,
                                                        message.reply_to_message.message_id, message.message_id)
            #chat_db.insert_message(message.chat.id, message.message_id + 1, 0, ' '.join(select_messages))
            await process_request({"select_messages": ' '.join(select_messages),
                                   'select_messages_count': select_messages_count,
                                   'chat_id': message.chat.id,
                                   'flag_output': 'tg_bot'})
            # await message.reply(' '.join(messages))
        else:
            await message.reply("Вы не выбрали сообщене!")


async def main():
    await dp.start_polling()


async def send_message(chat_id, text):
    await bot.send_message(chat_id, text)


async def process_request(data):
    severity = "sum"

    # Sending the message
    channel.basic_publish(
        exchange=EXCHANGE_NAME, routing_key=severity, body=json.dumps(data))

    print(f" [x] Sent {severity}:{data}")


if __name__ == '__main__':

    print("Bot started")
    amqp_url = os.environ['AMQP_URL']
    url_params = pika.URLParameters(amqp_url)
    url_params.heartbeat = 0

    # connect to rabbitmq
    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    asyncio.run(main())

    connection.close()
