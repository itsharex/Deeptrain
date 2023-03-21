from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("websocket/<str:token>/", im_websocket, name="websocket"),
]
