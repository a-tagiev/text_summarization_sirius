import random
from Bots.Summary.WithOutServer.Helpers.functions import make_summary, make_perfect_answer


def process_request(data, vk):
    out_summary = make_summary(data['select_messages'])
    out_message = make_perfect_answer(out_summary, data['select_messages_count'])
    send_message(chat_id=data['chat_id'], message=out_message, vk=vk)


def get_message_history(chat_id, start_message_id, vk):
    # Получаем историю сообщений начиная с начала
    messages = vk.messages.getHistory(
        peer_id=2000000000 + chat_id,
        start_message_id=start_message_id,
        count=200  # Максимальное количество сообщений, которое можно получить за один запрос
    )
    return messages['items']


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
