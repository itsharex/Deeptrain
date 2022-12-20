from applications.application import *


class SnakeServer(SiteServer):
    async def run(self):
        pass


class SnakeClient(SiteClient):
    async def receiveEvent(self, obj: Any):
        pass


@appManager.register
class Application(SiteApplication):
    server_type = SnakeServer
    client_type = SnakeClient
    port = 8001
