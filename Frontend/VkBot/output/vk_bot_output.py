import random
import vk_api
from pydantic import BaseModel

from Helpers.tokenBot import main_token
from Helpers.functions import make_perfect_answer

import json
import pika
import os

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()


QUEUE_NAME = "output_queue_VK"
EXCHANGE_NAME = "output_exchange"


def send_message(chat_id, message):
    vk.messages.send(
        random_id=random.randint(1, 100000),
        chat_id=chat_id,
        message=str(message)
    )


def input_message(data: json):
    summary_out = data['text_summary']
    chat_id = data['chat_id']
    summary_messages_count = data['select_messages_count']
    out_message = make_perfect_answer(summary_out, summary_messages_count)
    send_message(chat_id, out_message)

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

    try:
        data = json.loads(body.decode())
        input_message(data)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':

    print("Bot started")
    amqp_url = os.environ['AMQP_URL']
    url_params = pika.URLParameters(amqp_url)
    connection = pika.BlockingConnection(url_params)
    url_params.heartbeat = 0

    # # connect to rabbitmq
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host='rabbit_mq')
    # )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    result = channel.queue_declare(queue=QUEUE_NAME)

    severity = "vk_bot"

    channel.queue_bind(
            exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=severity)

    channel.basic_qos(prefetch_count=1)

    # define the queue consumption

    channel.basic_consume(
        queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    print("Waiting to consume")

    # start consuming
    channel.start_consuming()
