from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserChangePasswordForm, UserProfileForm
from .serializers import UserSerializer
from Deeptrain.settings import LOGIN_URL
from oauth.oauth import oauthManager
from utils.wraps import login_required, authenticated_redirect
from utils.router import register


@register("user")
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


@cache_page(60)
def index(request: WSGIRequest) -> HttpResponse:
    return render(request, "index.html")


@authenticated_redirect
def login(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        return UserLoginForm(request).as_response()
    else:
        return render(request, 'user/login.html',
                      {"form": UserLoginForm(request), "oauth": oauthManager.login_template})


@authenticated_redirect
def register(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        return UserRegisterForm(request).as_response()
    else:
        return render(request, 'user/register.html', {"form": UserRegisterForm(request)})


def logout(request: WSGIRequest) -> HttpResponse:
    auth.logout(request)
    return redirect(LOGIN_URL)


@login_required
def change(request: WSGIRequest, _) -> HttpResponse:
    if request.POST:
        return UserChangePasswordForm(request).as_response()
    else:
        return render(request, 'user/change.html', {"form": UserChangePasswordForm(request)})


@login_required
def home(request: WSGIRequest, user) -> HttpResponse:
    return render(request, "user/home.html", {"name": user.username})


@login_required
def profile(request: WSGIRequest, visitor) -> HttpResponse:
    if request.POST:
        return UserProfileForm(request).as_response()
    else:
        uid = request.GET.get("id")
        if uid and uid.isdigit():
            query = User.objects.filter(id=int(uid))
            if query.exists():
                user = query.first()
            else:
                raise Http404("The user was not found on this server.")
        else:
            user = visitor
        return render(request, "user/profile.html", {"user": user, "is_self": user == visitor,
                                                     "form": UserProfileForm(request)})
