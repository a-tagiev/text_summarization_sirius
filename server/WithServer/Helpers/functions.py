import asyncio
import aiohttp
from Bots.Summary.WithServer.Helpers.tokenBot import FastApi_URL


async def async_send_request_to_fastapi(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{FastApi_URL}/summarization_text", json=data) as response:
            # Проигнорируем ответ сервера
            pass


async def async_send_request(data):
    await async_send_request_to_fastapi(data)


def process_request(data):
    asyncio.run(async_send_request(data))


def check_ai_marker(original_string):
    return "Generate by dataminds" in original_string or "/summary" in original_string


def make_perfect_answer(summary_answer, select_messages_count):
    answer = f"""Результат суммаризации {select_messages_count} сообщений:

{summary_answer}

Generate by dataminds 
    """
    return answer
