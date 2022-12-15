from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from dwebsocket import require_websocket
from views import admin_required, ajax_required
from .monitor import monitor
from geoip.analysis import analysis_site_request


@admin_required
def index(request: WSGIRequest, user):
    return render(request, "monitor/dashboard.html", {"token": user.token})


@require_websocket
def monitor_websocket(request, token) -> None:
    monitor.add_client(request, token)


@ajax_required
@admin_required
def site_request(request: WSGIRequest, _):
    return JsonResponse(analysis_site_request(), safe=False)
