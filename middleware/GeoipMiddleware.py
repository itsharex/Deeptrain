from geoip.cache import countryCache
from geoip.geoip import get_ip
from monitor.monitor import monitor
from monitor.cache import requestCache
from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin


class GeoipMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(GeoipMiddleware, self).__init__(*args, **kwargs)

    @staticmethod
    def process_request(request: WSGIRequest):
        # request.country = countryCache(request)
        ip = get_ip(request)
        request.ip = ip
        request.country = countryCache.ip(ip)
        monitor.requests += 1
        requestCache.add()
        return
