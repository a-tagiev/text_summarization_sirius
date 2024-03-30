import random
import os

current_dir = os.path.dirname(os.path.realpath(__file__))


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


def check_lion_command(event, vk, upload):
    user_id = event.message['from_id']
    if str(user_id) == '242217382':
        photo = current_dir + '/Source/lion.jpeg'
        attachments = []
        upload_image = upload.photo_messages(photos=photo)[0]
        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
        vk.messages.send(
            random_id=random.randint(1, 100000),
            chat_id=event.chat_id,
            attachment=','.join(attachments)
        )
