from django.urls import path
from . import views
from .oauth import oauthManager as manager

urlpatterns = [
    path('bind/', views.bind, name="bind"),
] + manager.urlpatterns

