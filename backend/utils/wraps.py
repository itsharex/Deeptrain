from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required as _auth_login_required


def xml_required(_decorate_exec: callable) -> callable:
    def _exec_function(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
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
