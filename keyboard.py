from main import ch_bot
import json

def receive_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }

keyboard = {
    "one_time": False,
    "buttons": [
        [receive_button('поиск', 'primary')],
        [receive_button('старт', 'secondary')]
    ]
}

def sender(user_id, text):
    ch_bot.vk.method('messages.send', {'user_id': user_id,
                                    'message': text,
                                    'random_id': 0,
                                    'keyboard': keyboard})

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
