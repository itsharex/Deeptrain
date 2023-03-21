from utils.wraps import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from applications.application import appManager


@login_required
@cache_page(60)
def index(request: WSGIRequest, _) -> HttpResponse:
    return render(request, "applications/applications.html", {"templates": appManager.templates})
