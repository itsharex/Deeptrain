import json
from typing import List, Any, Union
import jwt.exceptions
from django.db.models import AutoField

from dwebsocket.backends.default import websocket
from DjangoWebsite.settings import CODING
from controller import webtoken_validate, get_user_from_name, get_profile_from_user
from user.models import User, Profile, identities


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
        self.group.remove_client(self)

    def connectEvent(self) -> None:
        pass

    def close(self) -> None:
        self.__sock.close()
        self.disconnectEvent()

    __del__ = close


class AbstractGroup(object):
    _socks: List[AbstractSocket]
    client_type: AbstractSocket = AbstractSocket

    def __init__(self):
        self._socks = []

    def append_client_to_socks(self, sock: client_type) -> client_type:
        self._socks.append(sock)
        return sock

    def add_client(self, request) -> client_type:
        return self.append_client_to_socks(self.client_type(request.websocket, self, _start=False)).listen()

    def remove_client(self, sock: client_type):
        if sock in self._socks:
            if sock.is_alive():
                sock.close()
            self._socks.remove(sock)
            return True
        return False

    def get_sockets(self) -> List[client_type]:
        return self._socks

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
        super(JSONSocket, self).send(json.dumps(data))

    def read(self) -> Union[Any, None]:
        _read = super(JSONSocket, self).read()
        return json.loads(_read) if _read else None

    def receiveEvent(self, obj) -> None:
        pass


class JSONGroup(AbstractGroup):
    _socks: List[JSONSocket]
    client_type = JSONSocket


class WebClient(JSONSocket):
    group: "WebClientGroup"

    def __init__(self, sock: websocket.DefaultWebSocket, user_obj: User, group: "AbstractGroup", _start: bool = False):
        super(WebClient, self).__init__(sock, group, _start)
        self.user: User = user_obj
        self.profile: Profile = get_profile_from_user(self.user)
        self.id: int = user_obj.id  # user_obj.id: int
        self.username = user_obj.username
        self.admin: bool = self.profile.is_admin()
        self.identity: str = identities.get(self.profile.identity)


class WebClientGroup(JSONGroup):
    _socks: List[WebClient]
    client_type = WebClient

    def append_client_to_socks(self, sock: client_type) -> client_type:
        return super(WebClientGroup, self).append_client_to_socks(sock)

    def add_client(self, request, token: str = "") -> Union[WebClient, bool]:
        try:
            _validate, username = webtoken_validate(token)
            if _validate:
                user = get_user_from_name(username)
                sock = self.append_client_to_socks(self.client_type(request.websocket, user, self, _start=False))
                self.joinEvent(sock)
                return sock.listen()
            return False
        except jwt.exceptions.DecodeError:
            return False

    def remove_client(self, sock: WebClient) -> bool:
        if super(WebClientGroup, self).remove_client(sock):
            self.leaveEvent(sock)
            return True
        return False

    def joinEvent(self, sock: WebClient) -> None:
        pass

    def leaveEvent(self, sock: WebClient) -> None:
        pass
