import random

import vk_api
from Bots.Summary.Server.vk_bot_output.token_bot import main_token

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()


def sender(chat_id, message):
    vk.messages.send(chat_id=chat_id, message=message, random_id=random.randint(1, 1000))