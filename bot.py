import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import Bots.Tonal.Helpers.bot_functions as bot
from Bots.Tonal.Helpers.tokenBot import main_token, group_id
import Bots.Tonal.Helpers.bot_texts as bot_messages
from Bots.Tonal.Model.model import tonality_predict

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)

print("Bot started")


def handle_request(event):
    if '[club225216088|@club225216088] т' == event.message['text']:
        tonal_command(event)
    if '[club225216088|@club225216088]' == event.message['text']:
        bot.send_message(event.chat_id, bot_messages.help_message, vk=vk)


def tonal_command(event):
    tagged_message = bot.find_tagged_message(event)  # ищем тегнутое сообщение
    tonality = tonality_predict(tagged_message['text'])
    bot.send_message(event.chat_id, tonality, vk=vk)


for start in longpoll.listen():
    if start.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if start.from_chat and start.message['from_id'] > 0:
            bot.send_message(start.chat_id, bot_messages.start_message, vk=vk)
            break

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Проверяем, что сообщение отправлено не ботом
        if event.from_chat and event.message['from_id'] > 0:
            handle_request(event)
