import json
import time

import pika
import requests


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

    try:
        urls = {"info": "http://127.0.0.1:8001/", "sum1": "http://127.0.0.1:8002/",
                "sum2": "http://127.0.0.1:8003/", "ton": "http://127.0.0.1:8004/"}
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


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='main_queue')
queue_name = result.method.queue

severities = {"info", "sum1", "sum2", "ton"}


for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=False)
print(f"start consuming")

channel.start_consuming()