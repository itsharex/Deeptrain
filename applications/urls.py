from django.shortcuts import render
from django.urls import path
from applications.application import appHandler
from views import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from applications import application

applications_templates = application.appHandler.get_templates()


@login_required
def applications_index(request: WSGIRequest, _) -> HttpResponse:
    return render(request, "applications.html", {"templates": applications_templates})


urlpatterns = [path("", applications_index, name="index")] + appHandler.as_wsgi_urlpatterns()
