from django.utils.translation import gettext as _
from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from .models import User
from .forms import UserRegisterForm, LoginForm, UserChangePasswordForm, UserProfileForm
from Deeptrain.settings import LOGIN_URL
from oauth.oauth import oauthManager
from utils.wraps import login_required, authenticated_redirect


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.data)
        if form.is_valid():
            if user := auth.authenticate(username=form.get("username"), password=form.get("password")):
                auth.login(request, user)
                return Response({
                    "status": True,
                    "message": _("Login successfully"),
                }, status=HTTP_200_OK)

            return Response({
                "status": False,
                "message": _("Authorization error"),
            }, status=HTTP_403_FORBIDDEN)

        return Response({
            "status": False,
            "message": _("Invalid parameters"),
        }, status=HTTP_400_BAD_REQUEST)


@authenticated_redirect
def login(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        return LoginForm(request).as_response()
    else:
        return render(request, 'user/login.html',
                      {"form": LoginForm(request), "oauth": oauthManager.login_template})


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
