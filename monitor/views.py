from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from views import admin_required


@admin_required
def index(request: WSGIRequest, _):
    return render(request, "monitor/dashboard.html")
