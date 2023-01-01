from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required as _auth_login_required
from django.views.decorators.cache import cache_page
from user.models import User
from user.forms import UserRegisterForm, UserLoginForm, UserChangePasswordForm, UserProfileForm
from DjangoWebsite.settings import LOGIN_URL
from oauth.oauth import oauthManager


def ajax_required(_decorate_exec: callable) -> callable:
    def _exec_function(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if request.is_ajax():
            return _decorate_exec(
                request,
                *args, **kwargs,
            )
        else:
            raise Http404("404")

    return _exec_function


def login_required(_decorate_exec: callable) -> callable:
    @_auth_login_required
    def _exec_function(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        return _decorate_exec(
            request,
            request.user,
            *args, **kwargs
        )

    return _exec_function


def authenticated_redirect(_decorate_exec: callable) -> callable:
    def _exec_function(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("/home/")
        else:
            return _decorate_exec(
                request,
                *args, **kwargs
            )
    return _exec_function


def identity_required(level: int):
    def _decorate_(_decorate_exec: callable) -> callable:
        @login_required
        def _exec_(request: WSGIRequest, user, *args, **kwargs):
            if user.identity >= level:
                return _decorate_exec(
                    request, user,
                    *args, **kwargs
                )
            else:
                return render(request, 'permission.html')

        return _exec_

    return _decorate_


vip_required = identity_required(1)
admin_required = identity_required(2)
owner_required = identity_required(3)


@cache_page(60)
def index(request: WSGIRequest) -> HttpResponse:
    return render(request, "index.html")


@authenticated_redirect
def login(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        return JsonResponse(UserLoginForm(request).get_response())
    else:
        return render(request, 'login.html', {"form": UserLoginForm(request), "oauth": oauthManager.login_template})


@authenticated_redirect
def register(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        return JsonResponse(UserRegisterForm(request).get_response())
    else:
        return render(request, 'register.html', {"form": UserRegisterForm(request)})


def logout(request: WSGIRequest) -> HttpResponse:
    auth.logout(request)
    return redirect(LOGIN_URL)


@login_required
def change(request: WSGIRequest, _) -> HttpResponse:
    if request.POST:
        return JsonResponse(UserChangePasswordForm(request).get_response())
    else:
        return render(request, 'change.html', {"form": UserChangePasswordForm(request)})


@login_required
def home(request: WSGIRequest, user) -> HttpResponse:
    return render(request, "home.html", {"name": user.username})


@login_required
def profile(request: WSGIRequest, visitor) -> HttpResponse:
    if request.POST:
        return JsonResponse(UserProfileForm(request).get_response())
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
        return render(request, "profile.html", {"user": user, "is_self": user == visitor,
                                                "form": UserProfileForm(request)})
