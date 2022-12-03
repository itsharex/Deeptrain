from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin
from geoip.geoip import *


class GeoipMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(GeoipMiddleware, self).__init__(*args, **kwargs)

    @staticmethod
    def process_request(request: WSGIRequest):
        print(get_city(request))
