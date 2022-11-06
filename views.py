from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
import controller
from model.forms import UserRegisterForm, UserLoginForm


def login_required(_decorate_exec: callable) -> callable:
    def _exec_function(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if controller.could_login_by_cookies(request):
            return _decorate_exec(
                request,
                controller.get_user_from_name(controller.get_userinfo_from_cookies(request)[0]),
                *args, **kwargs
            )
        else:
            return redirect("/login/")

    return _exec_function


def identity_required(level: int):
    def _decorate_(_decorate_exec: callable) -> callable:
        @login_required
        def _exec_(request: WSGIRequest, user, *args, **kwargs):
            _u_prof = controller.get_profile_from_user(user)
            if _u_prof.identity >= level:
                return _decorate_exec(
                    request, user,
                    *args, **kwargs
                )
            else:
                return redirect("/home/")
        return _exec_
    return _decorate_


vip_required = identity_required(1)
admin_required = identity_required(2)
owner_required = identity_required(3)


def index(request: WSGIRequest) -> HttpResponse:
    return render(request, "index.html",
                  {"username": controller.get_userinfo_from_cookies(request)[0]}
                  if controller.could_login_by_cookies(request) else {})


def login(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            return controller.set_cookies(
                redirect("/home/"),
                username=form.cleaned_data.get("username"),
                password=controller.encode_md5(form.cleaned_data.get("password")),
            )
        else:
            error = form.get_error()
            return render(request, 'login.html', {
                "form": form,
                "err_code": error,
            })
    else:
        return render(request, 'login.html', {"form": UserLoginForm()})


def register(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            return controller.set_cookies(
                redirect("/home/"),
                username=form.cleaned_data.get("username"),
                password=controller.encode_md5(form.cleaned_data.get("password")),
            )
        else:
            error = form.get_error()
            return render(request, 'register.html', {
                "form": form,
                "err_code": error,
            })
    else:
        return render(request, 'register.html', {"form": UserRegisterForm()})


def logout(request: WSGIRequest) -> HttpResponse:
    if controller.could_login_by_cookies(request):
        return controller.delete_cookies(render(request, 'login.html'), "username", "password")
    else:
        return redirect("/login/")


@login_required
def home(request: WSGIRequest, user) -> HttpResponse:
    username, password = user.username, user.password
    detail, identity = controller.get_profile_from_user(user).get_data(default_detail=controller.default_detail)
    if request.POST:
        detail = controller.update_data_from_user(user, detail=request.POST.get("text").strip()[:100])
    return render(request, "home.html", {"name": username, "profile": detail, "id": identity,
                                         "token": controller.webtoken_encode(username, password)})


def profile(request: WSGIRequest, uid) -> HttpResponse:
    result = controller.get_data_from_uid(uid)
    if result:
        user, (detail, identity) = result
        return render(request, "profile.html", {"name": user.username, "profile": detail, "id": identity})
    else:
        return HttpResponse("The user was not found on this server.")
