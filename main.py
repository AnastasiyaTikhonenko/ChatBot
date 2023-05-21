from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import comm_token

vk = vk_api.VkApi(token=comm_token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    })


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()

            if request == "привет":
                write_msg(event.user_id, f"Привет, друг")
            elif request == "пока":
                write_msg(event.user_id, "Пока :(")
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")
