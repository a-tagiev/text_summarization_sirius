import random
from Bots.Summary.WithOutServer.Helpers.functions import make_summary, make_perfect_answer


def find_tagged_message(event):
    # Проверяем, что сообщение содержит тег
    if 'reply_message' in event.message and 'action' not in event.message:
        return event.message['reply_message']
    return None


def send_message(chat_id, message, vk):
    vk.messages.send(
        random_id=random.randint(1, 100000),
        chat_id=chat_id,
        message=str(message)
    )
