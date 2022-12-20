import pickle
from websockets.legacy import server
import socket
import threadpool
from typing import *
import websockets
import asyncio


SITE_HOST = "127.0.0.1"


def is_open_port(host: str = SITE_HOST, port: int = 0) -> Tuple[int, bool]:
    """tcp detection function"""
    return port, not not socket.socket().connect_ex((host, port))


def get_not_open_ports(host: str, ports: List[int]) -> List[int]:
    """
    Get the ports that are not open
    :param host: IP host (str)
    :param ports: ports (list)
    :return: the ports that are not open (list)
    """

    pool = threadpool.ThreadPool(len(ports))
    responses = []
    tuple(map(
        pool.putRequest,
        threadpool.makeRequests(
            is_open_port,
            [((host, port), ()) for port in ports],
            callback=lambda request, response: responses.append(response[0]) if not response[1] else None,
        ),
    ))

    pool.wait()
    responses.sort()

    return responses


def _exec_detect_port(host: str, port: int, stride: int, max_limit: int) -> Tuple[bool, int]:
    while 0 <= port <= max_limit:
        if socket.socket().connect_ex((host, port)):
            return True, port
        port += stride
    return False, 0


def get_sample_open_ports(host: str, num: int, min_limit: int = 0, max_limit: int = 65535) -> List[Tuple[int]]:
    assert min_limit <= (min_limit + num - 1) <= max_limit, \
        f"Make sure the port range ({min_limit}~{max_limit}, total {num}) is between min(0) and max(65535)!"
    pool = threadpool.ThreadPool(num)
    responses = []
    tuple(map(
        pool.putRequest,
        threadpool.makeRequests(
            _exec_detect_port,
            [((host, min_limit + x, num, max_limit), ()) for x in range(num)],
            callback=lambda request, response: responses.append(response[1]) if response[0] else None,
        ),
    ))

    pool.wait()
    responses.sort()

    assert len(responses) == num, f"Insufficient available ports ({num})! Number of available ports {len(responses)}."
    return responses


def recv_pickle(_pickle):
    return pickle.loads(_pickle)


class AsyncServerClient(object):
    def __init__(self, websocket: server.WebSocketServerProtocol, parent):
        self.websocket = websocket
        self.parent: AsyncServer = parent
        self.is_alive = False

    async def listen(self):
        self.is_alive = True
        async for message in self.websocket:
            await self.parent.receive_from_websocket(self, message)
        self.is_alive = False

    async def send(self, message) -> bool:
        if self.is_alive:
            await self.websocket.send(message)
            return True
        return False

    async def send_pickle(self, obj):
        return await self.send(pickle.dumps(obj))


class AsyncServer(object):
    client_type = AsyncServerClient

    def __init__(self, port: int, allow_hosts=None):
        self.addr = [SITE_HOST, port]
        self.port = port
        self.loop = asyncio.new_event_loop()
        self.clients: List[AsyncServerClient] = []
        self.is_alive = False
        self.allow_hosts = set(allow_hosts or [SITE_HOST, "localhost", "127.0.0.1"])

    @property
    def alive_socket(self) -> Iterable[AsyncServerClient]:
        return iter(self.clients)

    def __iter__(self):
        return iter(self.clients)

    def __del__(self):
        self.clients = []

    def add_client(self, websocket: server.WebSocketServerProtocol):
        #  host validate
        host = websocket.remote_address[0]
        if host in self.allow_hosts:
            client = self.client_type(websocket, self)
            self.clients.append(client)
            return client.listen()
        else:
            websocket.close()

    async def _listen(self):
        self.is_alive = True
        async with websockets.serve(self.add_client, SITE_HOST, self.port, loop=self.loop):
            await asyncio.Future()
        self.is_alive = False

    def listen(self):
        self.loop.run_until_complete(self._listen())

    async def group_send(self, message):
        _clean_clients = []
        for client in self.clients:
            if not await client.send(message):
                _clean_clients.append(client)
        return tuple(map(self.clients.remove, _clean_clients))

    async def receive_from_websocket(self, client: AsyncServerClient, message):
        # await self.group_send(message)
        pass


class AsyncClient(object):
    def __init__(self, port: int, loop=None):
        self.port = port
        self.addr = [SITE_HOST, port]
        self.loop = loop or asyncio.new_event_loop()
        self.websocket = None

    async def _listen(self):
        async with websockets.connect(self.url, loop=self.loop) as self.websocket:
            async for message in self.websocket:
                await self._receiveEvent(message)

    def listen(self):
        return asyncio.run_coroutine_threadsafe(self._listen(), self.loop)

    @property
    def url(self) -> str:
        return f"ws://{SITE_HOST}:{self.port}/"

    async def _receiveEvent(self, message):
        # 未经处理的 recv
        pass

    async def send(self, message: Union[str, bytes]):
        return await self.websocket.send(message)

    async def send_pickle(self, obj):
        return await self.send(pickle.dumps(obj))
