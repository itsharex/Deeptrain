from threading import Thread
import logging
from typing import List, Tuple, Type
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from controller import webtoken_validate, get_user_from_name
from django import urls
from django.db import models
from DjangoWebsite.settings import APPLICATIONS_DIR, BASE_APPLICATION_DIR

logger = logging.getLogger(__name__)


class ApplicationHandler(object):
    def __init__(self):
        self.ApplicationsList: List[Tuple[AbstractApplication, Type[AbstractApplicationConsumer]]] = []
        self.__is_stp = False

    def add_app(self, app: "AbstractApplication", consumer: Type["AbstractApplicationConsumer"]):
        if isinstance(app, AbstractApplication) and issubclass(consumer, AbstractApplicationConsumer):
            self.ApplicationsList.append((app, consumer))
        return len(self.ApplicationsList)

    def get_app(self) -> Tuple[List["AbstractApplication"], List[Type["AbstractApplicationConsumer"]]]:
        return tuple(zip(*self.ApplicationsList)) if self.ApplicationsList else ([], [])

    def get_templates(self) -> List[dict]:
        return [app.get_template() for app in self.get_app()[0]]

    def register(self, app: Type["AbstractApplication"]):
        """
        @decorator

        register -> application -> consumer

        e.g.
        >>> @appHandler.register(UserApplication)
        >>> class MyConsumer(JSONApplicationConsumer):
        >>>     app: UserApplication
        >>>     def __init__(self):
        >>>         super().__init__()
        >>>         # TODO
        >>>

        """

        def consumer_connect(consumer: Type["AbstractApplicationConsumer"]):
            if app not in [type(__app) for __app in self.get_app()[0]]:
                _app = app()  # instantiate application
                app.index = self.add_app(_app, consumer)
                consumer.app = _app
            return consumer
        return consumer_connect

    def as_asgi_urlpatterns(self) -> List[urls.path]:
        return [urls.path(app.get_asgi_url(), consumer.as_asgi(), name=app.name)
                for app, consumer in self.ApplicationsList if app.ASGISupport]

    def as_wsgi_urlpatterns(self):
        return [urls.path(app.get_wsgi_url(), urls.include("applications.{}.urls".format(app.name)), name=app.name)
                for app, _ in self.ApplicationsList if app.WSGISupport]

    def run_app(self):
        if self.__is_stp is True:
            return
        for path in APPLICATIONS_DIR:
            _file = f"{path}.application"
            try:
                __import__(_file)
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"\n\tApplication {path}:\n\t\tNo application file <{_file}> !")

        for app, consumer in self.ApplicationsList:
            app.start()
            logger.info(f"{str(app)} started at <Thread {app.get_thread().ident}>")
        self.__is_stp = True

    @staticmethod
    def app_settings():
        return [f"applications.{app_path}" for app_path in APPLICATIONS_DIR]


appHandler = ApplicationHandler()


class AbstractApplication(object):
    """
    :param name
        Application name
    :param author
        Application author name
    :param github_addr
        GitHub repository address
        If the value is empty, the template will not display the github address.
            e.g.
            >>> github_addr="https://github.com/zmh-program/Zh-Website"
    :param profile
        Application profile
    :param image
        url

    :param WSGISupport, ASGISupport
         WSGISupport: Provides wsgi routing assignments  include( /applications/<app-name>/ )
            [i]: if [WSGISupport = False], Its WSGI namespace cannot be used in templates.
         ASGISupport: Provides asgi routing assignments ( /applications/<app-name>/ )
    """
    name = ""
    author = ""
    github_addr = ""
    profile = """..."""
    image = ""

    index = 0
    WSGISupport = True
    ASGISupport = True

    def __init__(self, *args, **kwargs):
        self._thread = Thread(target=self.run)
        self._thread.setDaemon(True)
        self._thread.setName(str(self))

    def run(self):
        pass

    def get_wsgi_url(self) -> str:
        return f"applications/{self.name}/" if self.WSGISupport else ""

    def get_asgi_url(self) -> str:
        return f"applications/{self.name}/" if self.ASGISupport else ""

    def start(self) -> None:
        return self._thread.start()

    def get_thread(self) -> Thread:
        return self._thread

    def join(self):
        self._thread.join()

    def get_template(self) -> dict:
        return {
            "name": self.name,
            "author": self.author,
            "github": self.github_addr,
            "profile": self.profile,
            "image": self.image,
            "path": self.get_wsgi_url(),
            "index": '%02d' % self.index,
        }

    def __int__(self) -> int:
        return self.index

    def __str__(self) -> str:
        return f"Application {self.name} <{self.index}>"


class AbstractApplicationConsumer(WebsocketConsumer):
    app: AbstractApplication
    group_name: str

    def __init__(self, *args, **kwargs):
        super(AbstractApplicationConsumer, self).__init__(*args, **kwargs)
        self.group_name = self.app.name

    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, *args):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # Send message to room group
        pass


class JSONApplicationConsumer(AbstractApplicationConsumer):
    app: "UserApplication"  # without String: not defined.
    object: models.Model

    def __init__(self, *args, **kwargs):
        super(JSONApplicationConsumer, self).__init__(*args, **kwargs)
        self.__login: bool = False
        self.username = ""
        self.id = 0

    def is_login(self) -> bool:
        return self.__login

    def loginEvent(self):
        """executed when the user logined."""
        pass

    def disconnectEvent(self):
        """excuted when the user left (login = True)."""
        pass

    def connect(self):
        super(JSONApplicationConsumer, self).connect()
        self.app.add_user(self)

    def disconnect(self, *args):
        super(JSONApplicationConsumer, self).disconnect()
        if self.__login:
            self.app.leaveEvent(self)
            self.disconnectEvent()
        self.app.remove_user(self)

    def bytes_data_handler(self, data: bytes):
        pass

    def json_data_handler(self, data: "python Object"):
        """ after <__login == true>"""
        pass

    def send_json(self, data=None, *args, **kwargs):
        """ send json data """
        super(JSONApplicationConsumer, self).send(json.dumps(data), *args, **kwargs)

    def send_bytes(self, data: bytes):
        super(JSONApplicationConsumer, self).send(bytes_data=data)

    def group_send(self, pydic: dict):
        """ send message to room group"""
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            pydic,
        )

    def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.bytes_data_handler(bytes_data)
        if text_data:
            data = json.loads(text_data)
            if not self.__login:
                success, username = webtoken_validate(data["token"])
                if not success:
                    async_to_sync(self.disconnect)()
                    return
                else:
                    self.username = username
                    self.object = get_user_from_name(username)
                    self.id = self.object.id
                    self.__login = True
                    self.app.joinEvent(self)
                    self.loginEvent()
            else:
                self.json_data_handler(data)


class UserApplication(AbstractApplication):
    def __init__(self, *args, **kwargs):
        super(UserApplication, self).__init__(*args, **kwargs)
        self.__users = []

    # @property
    # def users(self) -> List[ApplicationConsumer]:
    #     return self.__users
    #
    # @users.setter
    # def users(self, user: ApplicationConsumer) -> None:
    #     if isinstance(user, ApplicationConsumer):
    #         self.__users.append(user)
    #
    # @users.deleter
    # def users(self) -> None:
    #     self.__users = []

    def get_users(self) -> List[JSONApplicationConsumer]:
        return self.__users

    def get_user_length(self) -> int:
        return len(self.__users)

    def add_user(self, user: JSONApplicationConsumer):
        if isinstance(user, JSONApplicationConsumer):
            self.__users.append(user)

    def filter_user(self) -> set:
        return set(filter(lambda user: user.is_login(), self.__users))

    def get_avaliable_user_length(self) -> int:
        return len(self.filter_user())

    def remove_user(self, user: JSONApplicationConsumer):
        if user in self.__users:
            self.__users.remove(user)

    def joinEvent(self, user: JSONApplicationConsumer):
        pass

    def leaveEvent(self, user: JSONApplicationConsumer):
        pass
