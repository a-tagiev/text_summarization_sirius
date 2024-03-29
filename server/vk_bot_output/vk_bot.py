import vk_api
from . token_bot import main_token

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()


def sender(peer_id, message):
    vk.messages.send(peer_id=peer_id, message=message, random_id=0)
