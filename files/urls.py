from django.urls import path
from .views import *
urlpatterns = [
    path("", index, name="index"),
    path("upload/", upload, name="upload"),
    path("download/<int:uid>/<str:ufile>/", download, name="download"),
    path("search/", search, name="search"),
]
