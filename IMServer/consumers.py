import json
import time

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from controller import webtoken_validate, get_user_from_name, get_profile_from_user, identitys

room_number = 0
host = get_user_from_name("zmh")
host_profile = get_profile_from_user(host)
room_number_update = {
    'type': 'chat_message',
    'message': "",
    'id': host.id,
    'identity': identitys.get(host_profile.identity),
    'name': host.username,
    'html': False,
    'image_path': "https://cdn-icons-png.flaticon.com/128/6908/6908194.png",
}


def leave(username):
    message = room_number_update.copy()
    message["message"] = f"{username}离开了, 当前人数{room_number}."
    return message


def new(username):
    message = room_number_update.copy()
    message["message"] = f"{username}加入服务器, 当前人数{room_number}."
    return message


# 本来使用的是 AsyncWebsocketConsumer, 但是一部分函数无法配对 sync_to_async 或 channels.db.database_sync_to_async,
# 因而改用 WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    room_group_name: str

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.identity = ""
        self.admin = False
        self.username = ""
        self.is_login = False
        self.id = 0

    def connect(self):
        self.room_group_name = f"public_chat"
        self.is_login = False
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, *args):
        if self.is_login:
            global room_number
            room_number -= 1
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            leave(self.username)
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, *args):
        text_data_json = json.loads(text_data)
        if self.is_login:
            message = text_data_json['message'].strip()[:500]
            if not message:
                return
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'id': self.id,
                    'identity': self.identity,
                    'name': self.username,
                    'html': self.admin,
                    'image_path': "/static/images/chat_user.png",
                }
            )
        else:
            success, username = webtoken_validate(text_data_json['token'])
            if not success:
                async_to_sync(self.disconnect)()
            else:
                global room_number
                room_number += 1

                user = get_user_from_name(username)
                profile = get_profile_from_user(user)
                self.is_login = True
                self.username = username
                self.id = user.id
                self.identity = identitys.get(profile.identity)
                self.admin = profile.is_admin()
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    new(username)
                )

    # Receive message from room group
    def chat_message(self, event):
        if self.is_login:
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'username': event['name'],
                'id': event['id'],
                'image_path': event['image_path'],
                'content': event['message'],
                'self': event['id'] == self.id,
                'is_html': event['html'],
                'identity': event['identity'],
                'time': int(time.time()),
            }))
