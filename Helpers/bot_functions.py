from Helpers.tokenBot import FastApi_URL
import aiohttp
import asyncio


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


async def async_send_request_to_fastapi(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{FastApi_URL}/predict", json=data) as response:
            # Проигнорируем ответ сервера
            pass


async def async_send_request(data):
    await async_send_request_to_fastapi(data)


def process_request(data):
    asyncio.run(async_send_request(data))


