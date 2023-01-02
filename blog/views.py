from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from views import login_required


@login_required
def index(request: WSGIRequest, _):
    return render(request, "")
