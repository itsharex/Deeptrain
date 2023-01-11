from django.shortcuts import render
from .geoip import *
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from utils.wraps import xml_required, admin_required
from .analysis import analysis


@xml_required
@admin_required
def country(request: WSGIRequest, _):
    ip = request.GET.get("ip", None)
    return HttpResponse(str(get_country_name_from_ip(ip) if ip else get_country_name_from_request(request)))


@xml_required
@admin_required
def city(request: WSGIRequest, _):
    ip = request.GET.get("ip", None)
    return JsonResponse(get_city_from_ip(ip) if ip else get_city_from_request(request))


@xml_required
@admin_required
def analysis_request(request: WSGIRequest, _):
    return JsonResponse(analysis())


@admin_required
def index(request: WSGIRequest, _):
    return render(request, "geoip/geoip.html")
