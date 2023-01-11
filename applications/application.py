import asyncio
import os
import time
import warnings
from threading import Thread
from multiprocessing import Process
import logging
from typing import *
from inspect import currentframe, getmodule
from django.utils.functional import cached_property
from applications.config import json_parser, JSONConfig
from django import urls
from DjangoWebsite.settings import APPLICATIONS_DIR
from . import websocket_protocol as protocol

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

        self._native_app: List[AbstractApplication] = []
        self._sync_app: List[SyncApplication] = []
        self._async_app: List[AsyncApplication] = []
        self._proc_app: List[ProcessApplication] = []
        self._site_app: List[SiteApplication] = []

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
            elif isinstance(app, ProcessApplication):
                self._proc_app.append(app)
            elif isinstance(app, SiteApplication):
                self._site_app.append(app)
            else:
                self._native_app.append(app)

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

    def lazy_register(
            self,
            application: Type["SiteApplication"],
            server: Optional[Type["SiteServer"]] = None,
            client: Optional[Type["SiteClient"]] = None,
    ):
        """
        lazily initialize site application.

        :param server: subclass of SiteServer:
            `type`
            `default(SiteServer)`

        :param client: subclass of SiteClient
            `type`
            `default(SiteServer)`

        :param application: subclass of SiteApplication
            `type`

        :call:
            appManager.register

        :return:
            the instance of Application (depend on variable application)
        """
        if isinstance(application, SiteApplication):
            warnings.warn("\n\tThe application has already been initialized. "
                          "It can be registered using appManager.register(<app>).\n")
            return self.register(application)
        application = application()
        application.server_type = server or SiteServer
        application.client_type = client or SiteClient
        self.register(application)

        return application

    @cached_property
    def urlpatterns(self):
        """ Get the urlpatterns include all the applications. """

        return [urls.path(app.include_url, urls.include(("applications.{}.urls".format(app.name), app.name)),
                          name=app.name)
                for app in self.applications if app.config.UrlRoute]

    def setup_app(self):
        """ Initialize ApplicationManager. """
        assert not self.__is_stp, "ApplicationManager was already initialized!"

        for path in APPLICATIONS_DIR:
            _file = f"{path}.application"
            try:
                __import__(_file)
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f"\n\tApplication {path}:\n\t\tCannot import application from file {_file} !")
        self.__is_stp = True
        logger.debug(f"Initialize applications successfully.")

    @cached_property
    def _including_app_types(self):
        return f"{len(self._sync_app)} sync apps, " \
               f"{len(self._async_app)} async apps, " \
               f"{len(self._proc_app)} process apps, " \
               f"{len(self._site_app)} site apps, " \
               f"{len(self._native_app)} native apps"

    def run_app(self):
        for __sync in [*self._sync_app, *self._native_app, *self._proc_app]:
            __sync.start()

        for __async in self._async_app:
            __async.start(self.loop)

        for __site in self._site_app:
            __site.start(self.loop)

        self.loop_thread.start()

        logger.info(
            f"{self.length} {['application has been started', 'applications have been started'][self.length > 1]}"
            f" (including {self._including_app_types}).")

    def deploy_app(self):
        self.setup_app()
        self.run_app()

    def product_app(self):
        self.run_app()
        logger.info(f"start server at process {os.getpid()}.")

    def _get_application(self, _call_from: str) -> "AbstractApplication":
        return self._applications_calls.get(_call_from)

    def get_application(self) -> "AbstractApplication":
        _call = _get_called_module_file()
        return self._get_application(_call_from=_call)

    def get_application_config(self, name):
        for app in self.applications:
            if app.name == name:
                return app

    def __str__(self):
        return f"ApplicationManager({self._including_app_types})"


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

    def run(self):
        pass

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


class ProcessApplication(AbstractApplication):
    _process: Process

    def __init__(self, *_, **__):
        super().__init__()
        self._process = Process(target=self.run, daemon=True, name=str(self))

    def __str__(self) -> str:
        return f"Process Application {self.name} <{self.index}>"

    def run(self):
        pass

    def start(self, *_) -> None:
        self._process.start()

    def get_process(self) -> Process:
        return self._process

    def join(self):
        self._process.join()


class SiteServer(protocol.AsyncServer):
    def __init__(self, port):
        super().__init__(port, )
        self.thread = Thread(target=self.listen, daemon=True)

    async def run(self):
        pass

    def start(self) -> None:
        self.thread.start()
        run_loop = asyncio.new_event_loop()
        run_loop.run_until_complete(self.run())


class SiteClient(protocol.AsyncClient):
    def __init__(self, port, loop):
        super(SiteClient, self).__init__(port, loop)
        self.listen()


class SiteApplication(AbstractApplication):
    """
    C/S architecture.

    Client ≈ Async Application
    Server ≈ Process Application


    · structure of SiteApplication:

       |     -- public --         |  middleware  |           -- localhost --              |
       |    *.*.*.*    wss://xxx.site | ... |  127.0.0.1       ws://.:80      127.0.0.1   |
       | Website Client <-----------> | ... | Client App <-----------------> Server App   |
       |                              | ... |                                             |
       |          Browser             | ... |   Async Application    Process Application  |
       |<--                    B/S arch.              -->|<--      C/S arch.           -->|


    · Why use websocket protocol instead of native tcp socket?
        - Solve subcontracting, sticky package.

    """
    port: int

    client: SiteClient
    server: SiteServer

    client_type = SiteClient
    server_type = SiteServer

    _process: Process
    _thread: Thread

    def __init__(self):
        assert isinstance(self.port, int)
        super().__init__()

    def run_within_called_server(self, loop):
        r"""
        不从在父进程 初始化self.server的原因:
        
        Windows系统:
              File "#:\ProgramData\Anaconda3\envs\...\lib\multiprocessing\context.py", line 322, in _Popen
                return Popen(process_obj)
              File "#:\ProgramData\Anaconda3\envs\...\lib\multiprocessing\popen_spawn_win32.py", line 89, in __init__
                reduction.dump(process_obj, to_child)
              File "#:\ProgramData\Anaconda3\envs\...\lib\multiprocessing\reduction.py", line 60, in dump
                ForkingPickler(file, protocol).dump(obj)
            AttributeError: Can't pickle local object 'WeakSet.__init__.<locals>._remove'
            
            Traceback (most recent call last):
              File "<string>", line 1, in <module>
              File "#:\ProgramData\Anaconda3\envs\...\lib\multiprocessing\spawn.py", line 105, in spawn_main
                exitcode = _main(fd)
              File "#:\ProgramData\Anaconda3\envs\...\lib\multiprocessing\spawn.py", line 115, in _main
                self = reduction.pickle.load(from_parent)
            EOFError: Ran out of input
            
        Linux/Unix 系统:
                OSError: [Errno 98] error while attempting to bind on address ('127.0.0.1', ~): address already in use
                server = await self._create_server()
              File "/root/.pyenv/versions/3.9/lib/python3.7/asyncio/base_events.py", line 1505, in create_server
                raise OSError(err.errno, 'error while attempting '
                raise OSError(err.errno, 'error while attempting '
            AttributeError: '_UnixSelectorEventLoop' object has no attribute '_signal_handlers'
                raise OSError(err.errno, 'error while attempting '
            OSError: [Errno 98] error while attempting to bind on address ('127.0.0.1', ~): address already in use
                raise OSError(err.errno, 'error while attempting '
            OSError: [Errno 98] error while attempting to bind on address ('127.0.0.1', ~): address already in use


         我猜原因应该是 process之间不共享内存, 因而需要再启动一个python子进程, 但是再次过程中,
         实例中的 AsyncServer(中 _weakrefset.WeakSet的_remove方法)
         不能被pickle和反pickle, 因此抛出异常.

         那知道原因了就好办了,解决方案:
            1. 直接在子进程中运行的函数中 创建套接字的实例
            2. 异步loop不共享, 在父进程中创建
        """
        self._process = Process(target=self.run, daemon=True, )
        self._process.start()
        self.client = self.client_type(self.port, loop=loop)
        self.client.listen()

    def run(self):
        """
        Initialize server and Run as a server in the subprocess.
            -> call: %.run_application()
        """

        self.server = self.server_type(self.port)

        self.server.start()
        self.run_application()

    def run_application(self):
        """
        Run the application (Server) in the subprocess.

                override in subclass
        """
        pass

    def run_without_called_server(self, loop):
        self.client = self.client_type(self.port, loop=loop)
        return self.client.listen()

    #  不能有 cached_property
    @property
    def open(self):
        return protocol.is_open_port(port=self.port)[1]

    def start(self, loop, detect_open: bool = False, *_) -> None:
        if not detect_open:
            #  等价于 [self.run_without_called_server, self.run_within_called_server][self.open](loop)
            if self.open:
                self.run_within_called_server(loop)
            else:
                self.run_without_called_server(loop)
