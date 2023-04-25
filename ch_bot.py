from kom_imp import sender
from main import *

for event in ch_bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        sender(user_id, msg.lower())
        if request == 'поиск':
            creating_database()
            ch_bot.write_msg(user_id, f'Привет, {ch_bot.name(user_id)}')
            ch_bot.find_user(user_id)
            ch_bot.write_msg(event.user_id, f'Пара найдена, нажмите "старт"')
            ch_bot.find_persons(user_id, offset)
        elif request == 'старт':
            for i in line:
                offset += 1
                ch_bot.find_persons(user_id, offset)
                break
        else:
            ch_bot.write_msg(event.user_id, 'Не понял ваше сообщение')
