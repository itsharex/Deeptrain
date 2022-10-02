from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
import controller
from applications import application

applications_templates = application.appHandler.get_templates()


def login_required(_decorate_exec: callable) -> callable:
    def _exec_function(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if controller.could_login_by_cookies(request):
            return _decorate_exec(request, *args, **kwargs)
        else:
            return redirect("/login/")

    return _exec_function


@controller.with_encoding
def main(request: WSGIRequest) -> HttpResponse:
    return render(request, "main.html",
                  {"username": controller.get_userinfo_from_cookies(request)[0]} if controller.could_login_by_cookies(
                      request) else {})


@controller.with_encoding
def login(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        username, password = request.POST.get("username", None), request.POST.get("password", None)
        success, resp = controller.login(username, password)
        if success:
            return controller.set_cookies(redirect("/home/"), username=username,
                                          password=controller.encode_md5(password))
        else:
            return render(request, 'login.html', {"username": username, "password": password, "err_code": resp})
    else:
        return render(request, 'login.html')


@controller.with_encoding
def register(request: WSGIRequest) -> HttpResponse:
    if request.POST:
        username, password, re_password = request.POST.get("username", None), \
                                          request.POST.get("password", None), \
                                          request.POST.get("re_password")
        success, resp = controller.register(username, password, re_password)
        if success:
            return controller.set_cookies(redirect("/home/"), username=username,
                                          password=controller.encode_md5(password))
        else:
            return render(request, 'register.html', {"username": username, "password": password,
                                                     "re_password": re_password, "err_code": resp})
    else:
        return render(request, 'register.html')


@controller.with_encoding
def logout(request: WSGIRequest) -> HttpResponse:
    if controller.could_login_by_cookies(request):
        return controller.delete_cookies(render(request, 'login.html'), "username", "password")
    else:
        return redirect("/login/")


@controller.with_encoding
@login_required
def home(request: WSGIRequest) -> HttpResponse:
    username, password = controller.get_userinfo_from_cookies(request)
    user, (detail, identity) = controller.get_data_from_username(username)
    if request.POST:
        detail = controller.update_data_from_user(user, detail=request.POST.get("text").strip()[:100])
    return render(request, "home.html", {"name": username, "profile": detail, "id": identity,
                                         "token": controller.webtoken_encode(username, password),
                                         "templates": applications_templates})


@controller.with_encoding
def profile(request: WSGIRequest, uid) -> HttpResponse:
    result = controller.get_data_from_uid(uid)
    if result:
        user, (detail, identity) = result
        return render(request, "profile.html", {"name": user.username, "profile": detail, "id": identity})
    else:
        return HttpResponse("The user was not found on this server.")
