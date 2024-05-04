import json
import sys
from enum import Enum

import pika
import os
from pydantic import BaseModel

EXCHANGE_NAME = "output_exchange"


class SummaryInput(BaseModel):
    select_messages: str
    flag_output: str
    chat_id: int
    select_messages_count: int


class SummaryOutput(BaseModel):
    text_summary: str
    chat_id: int
    select_messages_count: int


def class_to_dict(obj):
    return obj.__dict__

def send_to_rabbitmq(data : SummaryOutput, severity):


    # read rabbitmq connection url from environment variable
    amqp_url = os.environ['AMQP_URL']
    url_params = pika.URLParameters(amqp_url)
    url_params.heartbeat = 0


    # connect to rabbitmq
    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # Sending the message
    channel.basic_publish(
        exchange=EXCHANGE_NAME, routing_key=severity, body=json.dumps(data, default=class_to_dict).encode())

    print(f" [x] Sent {severity}:{data}")
