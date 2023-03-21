from django.urls import path
from applications.application import appManager
from .views import index

urlpatterns = [
    path("", index, name="index"),
    * appManager.urlpatterns,
]
