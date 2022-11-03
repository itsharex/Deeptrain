"""DjangoWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
import views
from django.conf import settings
from IMServer.views import chat

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="/static/images/favicon.ico")),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    path("", views.main),
    path("admin/", admin.site.urls),
    path("register/", views.register),
    path("login/", views.login),
    path("logout/", views.logout),
    path("home/", views.home),
    path("profile/id=<int:uid>", views.profile),
    path("chat/<str:token>/", chat),
    path("applications/", include("applications.urls"), name="applications"),
]
