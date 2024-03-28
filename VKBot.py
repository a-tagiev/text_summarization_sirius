import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from Model.model import summarize_text

# Укажите токен вашего сообщества VK
token = 'vk1.a.EWzgRDyuBxOuLGtHqS-S6vwyjGKZWsWjJ3WbyY2AhHJhfO_AszbEV1oDIXk83zX62zekUZzGNyS8qzXT1bvjH7kHyGWomE3KOzwmRQePJyXizInKu46W3vR6mXVWacdShVwYQpyCbYRBIp1pq1qI28IggEU3pUcCmhI17XmlThlDiDrB6xR5AzDf7W-ZmNQd-VZZBvJ6hi6Mx97_J2_kRw'
# Укажите ID вашего сообщества VK
group_id = '225246870'

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)

print("Bot started")


def get_message_history(chat_id, start_message_id):
    # Получаем историю сообщений начиная с начала
    messages = vk.messages.getHistory(
        peer_id=2000000000 + chat_id,
        start_message_id=start_message_id,
        count=200 # Максимальное количество сообщений, которое можно получить за один запрос
    )
    return messages['items']


def find_tagged_message(event):
    # Проверяем, что сообщение содержит тег
    if 'reply_message' in event.message and 'action' not in event.message:
        return event.message['reply_message']
    return None


def handle_command(event):
    if '/summary' in event.message['text']:
        summary_command(event)


def summary_command(event):
    tagged_message = find_tagged_message(event)  # ищем тегнутое сообщение
    if tagged_message:
        chat_id = event.chat_id
        start_message_id = tagged_message['date']  # беру айди тегнутого - стартового собщения
        messages = get_message_history(chat_id, start_message_id)  # беру все сообщения

        select_messages = ""
        select_messages_count = 0

        for message in messages[::-1]:  # перебираю все сообщения чата :(
            if message['date'] >= start_message_id:  # только сообщения, которые поступили после тегнутого
                if not check_ai_marker(message['text']):
                    select_messages += message['text'] + " "  # пополняю текст для суммаризации
                    select_messages_count += 1

        summary_answer = make_summary(select_messages)
        output_message = make_perfect_answer(summary_answer, select_messages_count)

        vk.messages.send(
            random_id=random.randint(1, 100000),
            chat_id=event.chat_id,
            message=str(output_message)
        )


def check_ai_marker(original_string):
    if "Generate by dataminds" in original_string or "/summary" in original_string:
        return True
    else:
        return False


def make_summary(text_to_summary):
    out = summarize_text(text_to_summary)
    return out


def make_perfect_answer(summary_answer, select_messages_count):
    answer = f"""Результат суммаризации {select_messages_count} сообщений:
    
{summary_answer}
    
Generate by dataminds 
    """
    return answer


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if event.from_chat and event.message['from_id'] > 0:
            handle_command(event)
