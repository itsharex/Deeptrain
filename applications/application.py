import asyncio
import os
import time
from threading import Thread
import logging
from typing import *
from inspect import currentframe, getmodule
from django.utils.functional import cached_property
from django.core.cache import cache
from applications.config import json_parser, JSONConfig
from django import urls
from DjangoWebsite.settings import APPLICATIONS_DIR


logger = logging.getLogger(__name__)


def _get_called_module_file():
    _frame = currentframe()
    current_mod = getmodule(currentframe()).__file__

    while True:
        _frame = _frame.f_back
        _mod = getmodule(_frame).__file__
        if _mod != current_mod:
            return _mod


def _get_called_module_dir():
    return os.path.dirname(_get_called_module_file())


class ApplicationManager(object):
    """
    register application:
    >>> @appManager.register
    >>> class MyApp(AbstractApplication):
    >>>     # TODO
    >>>
    """

    def __init__(self):
        self.applications: List[AbstractApplication] = []
        self._applications_calls: Dict[str, AbstractApplication] = {}
        self.__is_stp = False
        # gunicorn 中 worker不存在 event loop (django 在当前线程 Dummy-n 报错)
        # 默认情况下, 在主线程中时, 若没有event loop, 则 asyncio 会自动创建一个新的
        # 而在一个其他线程中, 则不会自动创建. 因此在新线程中，需要手动设置一个 event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop_thread = Thread(target=self.loop.run_forever)
        self.loop_thread.setDaemon(True)

        self._sync_app: List[SyncApplication] = []
        self._async_app: List[AsyncApplication] = []

    @cached_property
    def length(self):
        """
        Get the number of applications
        """

        return len(self.applications)

    def add_app(self, app: "AbstractApplication"):
        if isinstance(app, AbstractApplication):
            _call = _get_called_module_file()

            self.applications.append(app)
            assert _call not in self._applications_calls, "Multiple apps are registered in the same app directory!"
            self._applications_calls[_call] = app
            if isinstance(app, AsyncApplication):
                self._async_app.append(app)
            elif isinstance(app, SyncApplication):
                self._sync_app.append(app)
        return len(self.applications)

    @cached_property
    def templates(self) -> List[dict]:
        """
        Get the templates of all the applications.
        """

        return [app.template for app in self.applications]

    def register(self, app: Union[Type["AbstractApplication"], "AbstractApplication"]):
        """
        Register applications (decorator)
        """
        if isinstance(app, AbstractApplication) and app not in self.applications:
            app.index = self.add_app(app)
        elif issubclass(app, AbstractApplication) and app not in map(type, self.applications):
            _app = app()  # instantiate application
            _app.index = self.add_app(_app)
        else:
            raise ValueError
        return app

    @cached_property
    def urlpatterns(self):
        """
        Get the urlpatterns include all the applications.
        """

        return [urls.path(app.include_url, urls.include(("applications.{}.urls".format(app.name), app.name)),
                          name=app.name)
                for app in self.applications if app.config.UrlRoute]

    def setup_app(self):
        """
        Initialize ApplicationManager.
        """
        assert not self.__is_stp, "ApplicationManager was already initialized!"

        for path in APPLICATIONS_DIR:
            _file = f"{path}.application"
            try:
                __import__(_file)
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"\n\tApplication {path}:\n\t\tCannot import application from file {_file} !")
        self.__is_stp = True
        logger.debug(f"Initialize applications successfully.")

    def run_app(self):
        for __sync in self._sync_app:
            __sync.start()

        for __async in self._async_app:
            __async.start(self.loop)
        self.loop_thread.start()

        if self.length == 1:
            logger.info(f"{self.length} application has been started.")
        elif self.length > 1:
            logger.info(f"{self.length} applications have been started.")

    def deploy_app(self):
        self.setup_app()
        self.run_app()

    def product_app(self):
        if cache.get("start-application") is True:
            self.run_app()
            logger.info(f"start server at process {os.getpid()}.")
        else:
            cache.set("start-application", True, timeout=10)

    def _get_application(self, _call_from: str) -> "AbstractApplication":
        return self._applications_calls.get(_call_from)

    def get_application(self) -> "AbstractApplication":
        _call = _get_called_module_file()
        return self._get_application(_call_from=_call)


appManager = ApplicationManager()


class AbstractApplication(object):
    """
    :param name
        Application name
    :param author
        Application author name
    :param github_addr
        GitHub repository address
    :param profile
        Application profile
    :param InfoHtml
        like //img.shields.io/
    :param image
        url
    :param UrlRoute
        Provides wsgi routing assignments  include( /applications/<app-name>/ )
            [i]: if [UrlRoute = False], Its WSGI namespace cannot be used in templates.

    """

    index = 0
    config: JSONConfig

    def __init__(self, *_, **__):
        self.config = json_parser(_get_called_module_dir())
        assert self.config

    @cached_property
    def include_url(self) -> str:
        return f"{self.name}/" if self.config.UrlRoute else ""

    @cached_property
    def wsgi_url(self) -> str:
        return f"/applications/{self.name}/" if self.config.UrlRoute else ""

    def start(self, *_) -> None:
        pass

    def run(self):
        pass

    @cached_property
    def template(self) -> dict:
        return {
            **self.config.get_dict(),
            "path": self.wsgi_url,
            "index": '%02d' % self.index,
        }

    def __int__(self) -> int:
        return self.index

    def _set_name(self, name: str) -> None:
        self.config.name = name

    def _get_name(self) -> str:
        return self.config.name

    name = property(_get_name, _set_name, doc="Application Name")

    def __str__(self) -> str:
        return f"Application {self.name} <{self.index}>"


class SyncApplication(AbstractApplication):
    _thread: Thread

    def __init__(self, *_, **__):
        super().__init__()
        self._thread = Thread(target=self.run)
        self._thread.setDaemon(True)
        self._thread.setName(str(self))

    def __str__(self) -> str:
        return f"Sync Application {self.name} <{self.index}>"

    def start(self, *_) -> None:
        self._thread.start()

    def get_thread(self) -> Thread:
        return self._thread

    def join(self):
        self._thread.join()


class IntervalSyncApplication(SyncApplication):
    interval = 0.1  # second

    def run_once(self):
        pass

    def run(self):
        while 1:
            self.run_once()
            time.sleep(self.interval)


class AsyncApplication(AbstractApplication):
    def __init__(self, *_, **__) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"Async Application {self.name} <{self.index}>"

    async def run(self):
        pass

    def start(self, loop: asyncio.AbstractEventLoop):
        asyncio.run_coroutine_threadsafe(
            self.run(),
            loop,
        )


class IntervalAsyncApplication(AsyncApplication):
    interval = 0.1  # second

    async def run_once(self):
        pass

    async def run(self):
        while 1:
            await self.run_once()
            await asyncio.sleep(self.interval)
