from django.urls import path
from .views import *
urlpatterns = [
    path("upload/", upload, name="upload"),
    path("download/<int:uid>/<str:ufile>/", download, name="download"),
]
