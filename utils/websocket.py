import json
from typing import List, Any, Union
import jwt.exceptions
from django.utils.functional import cached_property

from dwebsocket.backends.default import websocket
from DjangoWebsite.settings import CODING
from utils.webtoken import validate_token
from user.models import User, Profile


class AbstractSocket(object):
    group: "AbstractGroup"

    def __init__(self, sock: websocket.DefaultWebSocket, group: "AbstractGroup", _start: bool = False):
        self.__sock = sock
        self.group = group
        self.connectEvent()
        if _start:
            self.listen()

    def get_socket(self) -> websocket.DefaultWebSocket:
        return self.__sock

    def read(self) -> Union[str, None]:  # inherit
        _read = self.__sock.read()
        return _read.decode(CODING).strip() if isinstance(_read, bytes) else None

    def is_alive(self) -> bool:
        return not self.__sock.is_closed()

    def listen(self):
        while self.is_alive():
            _read = self.read()
            if _read is not None:
                self.receiveEvent(_read)
        self.disconnectEvent()
        return self

    def send(self, string: str) -> None:
        if self.is_alive():
            return self.__sock.send(string)

    def receiveEvent(self, string) -> None:
        pass

    def disconnectEvent(self) -> None:
        pass

    def connectEvent(self) -> None:
        pass

    def close(self) -> None:
        self.__sock.close()
        self.disconnectEvent()

    __del__ = close


# class BaseValidation(object):
#     def __init__(self):
#         pass
#
#     def validate(self, request, obj: "BaseValidation" = None) -> bool:
#         return True
#
#
# class LoginRequiredValidation(BaseValidation):
#     def __init__(self):
#         super().__init__()
#
#     def validate(self, request, obj=None) -> bool:
#         cls = obj or self
#         token = request.GET.get("token") or request.POST.get("token")
#         result = validate_token(token)
#         if result:
#             setattr(cls, "username", result)
#             return True
#         else:
#             return False


class AbstractGroup(object):
    client_type = AbstractSocket

    #  sockets: List[client_type]

    def __init__(self):
        self.sockets = []

    def add_client(self, request) -> client_type:
        sock = self.client_type(request.websocket, self, _start=False)
        self.sockets.append(sock)
        return sock.listen()

    def remove_client(self, sock: client_type):
        if sock in self.sockets:
            if sock.is_alive():
                sock.close()
            self.sockets.remove(sock)
            return True
        return False

    def get_sockets(self) -> List[client_type]:
        return self.sockets

    def get_available_clients(self) -> List[client_type]:
        return list(filter(lambda sock: sock.is_alive(), self.get_sockets()))

    def get_available_clients_length(self) -> int:
        return len(self.get_available_clients())

    def group_send(self, data):
        for sock in self.get_available_clients():
            sock.send(data)

    def close(self):
        for sock in self.get_available_clients():
            sock.close()

    __del__ = close


class JSONSocket(AbstractSocket):
    group: "JSONGroup"

    def send(self, data: Any) -> None:
        super().send(json.dumps(data))

    def read(self) -> Union[Any, None]:
        _read = super().read()
        return json.loads(_read) if _read else None

    def receiveEvent(self, obj) -> None:
        pass


class JSONGroup(AbstractGroup):
    client_type = JSONSocket

    def __init__(self):
        super().__init__()


class WebClient(JSONSocket):
    group: "WebClientGroup"

    def __init__(self, sock: websocket.DefaultWebSocket, user: User, group: "AbstractGroup", _start: bool = False):
        super().__init__(sock, group, _start)
        self.user: User = user
        self.id: int = user.id
        self.username = user.username
        self.admin: bool = self.user.is_admin
        self.identity: str = self.user.real_identity

    @cached_property
    def profile(self) -> Profile:
        return self.user.profile

    def is_same(self, sock: "WebClient") -> bool:
        return sock.id == self.id


class WebClientGroup(JSONGroup):
    """
    Login required. (JWT validate)
    """

    client_type = WebClient
    level_required: int = 0

    def __init__(self):
        super().__init__()

    def add_client(self, request, token: str = "") -> Union[WebClient, None]:
        try:
            user = validate_token(token)
            if user and user.identity >= self.level_required:
                user: User
                sock = self.client_type(request.websocket, user, self, _start=False)
                self.detect_client(sock)
                self.sockets.append(sock)
                self.joinEvent(sock)
                return sock.listen()
        except jwt.exceptions.DecodeError:
            return

    def detect_client(self, target: WebClient):
        for sock in self.sockets:
            if target.is_same(sock):
                return self.existEvent(sock)

    def remove_client(self, sock: WebClient, silence=False) -> bool:
        if super(WebClientGroup, self).remove_client(sock):
            if silence:
                self.leaveEvent(sock)
            return True
        return False

    def joinEvent(self, sock: WebClient) -> None:
        pass

    def leaveEvent(self, sock: WebClient) -> None:
        pass

    def existEvent(self, sock: WebClient) -> None:
        pass
