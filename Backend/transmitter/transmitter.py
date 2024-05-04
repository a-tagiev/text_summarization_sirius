import json

import pika
import time
import os

import requests


QUEUE_NAME = "main_queue"
EXCHANGE_NAME = "input_exchange"

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)
url_params.heartbeat = 0

connection = pika.BlockingConnection(url_params)

# # connect to rabbitmq
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='rabbit_mq')
# )
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

result = channel.queue_declare(queue=QUEUE_NAME)



def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

    try:
        urls = {"info": "http://nginx:8001", "sum": "http://nginx:8002"}
        url = urls[method.routing_key]
        message = json.loads(body.decode())
        response = requests.post(url, json=message)
        if response.status_code == 200:
            print('Request successfully sent')
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print(f'Failed to send request to the server {response.status_code}')
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


severities = {"info", "sum"}


for severity in severities:
    channel.queue_bind(
        exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=severity)

channel.basic_qos(prefetch_count=1)


channel.basic_consume(
    queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

print("Waiting to consume")

channel.start_consuming()
