from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("ajax/", site_request, name="ajax"),
    path("websocket/<str:token>/", monitor_websocket, name="websocket"),
]
