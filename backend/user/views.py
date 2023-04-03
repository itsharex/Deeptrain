from django.utils.translation import gettext as _
from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from .models import User
from .forms import RegisterForm, LoginForm, UserChangePasswordForm, UserProfileForm
from Deeptrain.settings import LOGIN_URL
from oauth.oauth import oauthManager
from utils.wraps import login_required


@api_view(['POST'])
def login(request):
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
        "message": form.error,
    }, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    form = RegisterForm(request.data)
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
        "message": form.error,
    }, status=HTTP_400_BAD_REQUEST)

    user_submit_detection(self.request, "register")
    user_ip_detection(self.request)
    if User.objects.filter(username=username).exists():
        raise ValidationError("The user already exists!")

    user = User.objects.create_user(username=username, password=password, identity=0,
                                    country=getattr(self.request, "country"))
    Profile.objects.create(user=user, ip=getattr(self.request, "ip"))
    auth.login(self.request, user)
    if request.POST:
        return UserRegisterForm(request).as_response()
    else:
        return render(request, 'user/register.html', {"form": UserRegisterForm(request)})


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
