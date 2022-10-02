from django.urls import path
import IMServer.consumers
from applications.application import appHandler

websocket_urlpatterns = [
    path("chat/", IMServer.consumers.ChatConsumer.as_asgi(), name="chat")
] + appHandler.as_asgi_urlpatterns()
