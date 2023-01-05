from datetime import timedelta
import psutil
from typing import *
from DjangoWebsite.settings import MONITOR_INTERVAL
from utils.websocket import WebClientGroup, WebClient
from utils.loop import loop


class Monitor(WebClientGroup):
    level_required = 2  # Admin Level Required

    def __init__(self):
        super().__init__()
        self.requests = 0
        self.disk_percent = 0

        net_io = psutil.net_io_counters()
        self.recv = net_io.bytes_recv
        self.send = net_io.bytes_sent

        self._hooks = []
        self._update = 0

        loop.job(interval=timedelta(seconds=MONITOR_INTERVAL))(self.update)

    def reset(self):
        self.requests = 0

    def long_time_detection(self) -> None:
        self.disk_percent = psutil.disk_usage("/").percent

    @property
    def cpu_percent(self) -> float:
        return psutil.cpu_percent()

    @property
    def ram_percent(self) -> float:
        return psutil.virtual_memory().percent

    @property
    def offset(self) -> Tuple[int, int]:
        net_io = psutil.net_io_counters()
        sent = net_io.bytes_sent
        recv = net_io.bytes_recv

        sent_offset = sent - self.send
        recv_offset = recv - self.recv

        self.send = sent
        self.recv = recv

        return sent_offset, recv_offset

    def add_hook(self, hook):
        assert callable(hook)
        hook(self.initialize_data)
        self._hooks.append(hook)

    def remove_hook(self, hook):
        if hook in self._hooks:
            self._hooks.remove(hook)

    @property
    def initialize_data(self) -> dict:
        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "recv": self.recv,
            "send": self.send,
            "disk": self.disk_percent,
            "request": 0,
        }

    @property
    def update_data(self) -> dict:
        if self._update > 100:
            self.long_time_detection()
            self._update = 0

        sent_offset, recv_offset = self.offset

        result = {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "recv": recv_offset,
            "send": sent_offset,
            "disk": self.disk_percent,
            "request": self.requests,
        }
        self.reset()
        return result

    def update(self) -> Set[None]:
        response = self.update_data
        return set(map(lambda _hook: _hook(response), self._hooks))

    def joinEvent(self, sock: WebClient) -> None:
        self.add_hook(sock.send)

    def leaveEvent(self, sock: WebClient) -> None:
        self.remove_hook(sock.send)


monitor = Monitor()
