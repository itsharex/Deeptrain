from django.shortcuts import render
from django.urls import path
from django.views.decorators.cache import cache_page
from applications.application import appManager
from views import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse


@login_required
@cache_page(60)
def applications_index(request: WSGIRequest, _) -> HttpResponse:
    return render(request, "applications.html", {"templates": appManager.templates})


urlpatterns = [path("", applications_index, name="index")] + appManager.urlpatterns
