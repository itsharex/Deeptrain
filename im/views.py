import time
from typing import *
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from dwebsocket import require_websocket
from utils import websocket
from utils.wraps import login_required
from utils.audit import audit


ROBOT_IMAGE = "https://cdn-icons-png.flaticon.com/128/8811/8811373.png"


class IMClient(websocket.WebClient):
    group: "IMServerClientGroup"

    def __init__(self, *args, **kwargs):
        super(IMClient, self).__init__(*args, **kwargs)

    def receiveEvent(self, obj: dict) -> None:
        if isinstance(obj, dict):
            message = str(obj.get("message", "")).strip()[:500]
            if message and audit.strict_execute(message):
                self.group.group_send(self, message)
            else:
                self.group.host_send("评论内容含有违禁词", [self, ])

    def send(self, username="", message="", uid=0, image="", is_html: bool = False, identity: str = "User") -> None:
        super(IMClient, self).send({
            'username': username,
            'id': uid,
            'image': image,
            'content': message,
            'self': uid == self.id,
            'html': is_html,
            'identity': identity,
            'time': int(time.time()),
        })


class IMServerClientGroup(websocket.WebClientGroup):
    client_type = IMClient

    def __init__(self):
        super().__init__()

    def host_send(self, message="", clients: Optional[List[IMClient]] = None):
        for client in clients or self.get_available_clients():
            client: IMClient
            client.send("Chat Robot", message, -1, ROBOT_IMAGE, False, "Server-Owner")

    def group_send(self, sender: IMClient, message=""):
        for client in self.get_available_clients():
            client: IMClient
            client.send(
                sender.username,
                message,
                client.id,
                sender.profile.avatar.url, client.admin,
                client.identity
            )

    def leaveEvent(self, client: IMClient):
        self.host_send(f"{client.username} 离开了, 当前人数 {self.get_available_clients_length()}.")

    def joinEvent(self, client: IMClient):
        self.host_send(f"{client.username} 加入服务器, 当前人数 {self.get_available_clients_length()}.")

    def existEvent(self, sock: IMClient) -> None:
        self.host_send("您已在另一端建立链接,  如若想重新登录, 请刷新页面.")
        self.remove_client(sock, silence=True)


group = IMServerClientGroup()


@require_websocket
def im_websocket(request, token) -> None:
    group.add_client(request, token)


@login_required
def index(request: WSGIRequest, user) -> HttpResponse:
    return render(request, "im/index.html", {"token": user.token})
