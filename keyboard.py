import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from tables import *
from config import comm_token, my_token
from main import VkTools
import json


class BotInterface():
    def __init__(self, comm_token, my_token):
        self.vk = vk_api.VkApi(token=comm_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(my_token)
        self.params = {}
        self.worksheets = []
        self.offset = 0
        self.position = 0

    def message_send(self, user_id, message, attachment=None, keyboard=None):
        result = self.vk.method('messages.send',
                                {'user_id': user_id,
                                 'message': message,
                                 'attachment': attachment,
                                 'keyboard': keyboard,
                                 'random_id': get_random_id()}
                                )
        print(result)

    def buttons(self, user_id, message):
        keyb = {"one_time": True, "buttons": []}
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'keyboard': json.dumps(keyb),
                        'random_id': get_random_id()}
                       )

    # event handling / receive msg

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    '''Receive user's data'''
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    self.message_send(
                        event.user_id, f'Привет, {self.params["name"]}')
                elif event.text.lower() == 'поиск' or event.text.lower() == 'следующий':
                    self.message_send(
                        event.user_id, 'Начинаем поиск')
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    settings = dict(one_time=False, inline=True)
                    keyboard = VkKeyboard(**settings)
                    keyboard.add_button(label="поиск", color=VkKeyboardColor.POSITIVE)
                    keyboard.add_button(label="следующий", color=VkKeyboardColor.SECONDARY)
                    candidate = search(self, event)
                    while not check_if_seen(event.user_id, candidate["id"]) is None:
                        candidate = search(self, event)

                    self.message_send(
                        event.user_id,
                        candidate["message"],
                        attachment=candidate["attachment"],
                        keyboard=keyboard.get_keyboard()
                    )

                    insert_seen(event.user_id, candidate["id"])
                    'add worksheets to the data base according to event.user_id'

                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'До встречи')
                else:
                    self.message_send(
                        event.user_id, 'Неизвестная команда')


def search(self, event):
    if self.worksheets:
        worksheet = self.worksheets.pop()
        photos = self.vk_tools.get_photos(worksheet['id'])
        photo_string = ''
        for photo in photos:
            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
        self.position += 1
        if self.position > len(self.worksheets):
            self.worksheets = None
    else:
        self.worksheets = self.vk_tools.search_worksheet(
            self.params, self.offset)

        worksheet = self.worksheets.pop()
        'check worksheets to the data base according to event.user_id'

        photos = self.vk_tools.get_photos(worksheet['id'])
        photo_string = ''
        for photo in photos:
            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
        self.position = 0
        self.offset += len(self.worksheets)
        print(f'New offset is {self.offset}')

    return {'id': worksheet["id"],
            'message': f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}',
            'attachment': photo_string}


if __name__ == '__main__':
    bot_interface = BotInterface(comm_token, my_token)
    create_db()
    bot_interface.event_handler()
