from django.core.handlers.wsgi import WSGIRequest
from dwebsocket import require_websocket


@require_websocket
def chat(request) -> None:
    pass
