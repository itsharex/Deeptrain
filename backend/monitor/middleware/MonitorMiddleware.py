from DjangoWebsite.settings import CODING
from geoip.cache import countryCache
from geoip.geoip import get_ip
from ..monitor import monitor
from ..cache import requestCache
from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin


class MonitorMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(MonitorMiddleware, self).__init__(*args, **kwargs)
        self.coding = CODING

    def process_request(self, request: WSGIRequest):
        request.encoding = self.coding
        ip = get_ip(request)
        request.ip = ip
        request.country = countryCache.ip(ip)
        monitor.requests += 1
        requestCache.add()
        return
