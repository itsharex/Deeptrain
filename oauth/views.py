from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from views import login_required
from .oauth import oauthManager


@login_required
def bind(request: WSGIRequest, user):
    return render(request, "oauth/bind.html", {"oauth": oauthManager.bind_template(user)})
