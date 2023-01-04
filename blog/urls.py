from django.urls import path
from .views import *


urlpatterns = [
    path("", BlogSearchView(), name="index"),
    path("article/<int:idx>/", article, name="article"),
    path("submit/like/<int:idx>/", like, name="like"),
    path("submit/comment/<int:idx>/", comment, name="comment"),
]
