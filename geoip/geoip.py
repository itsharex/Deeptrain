from typing import *
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from geoip2.errors import GeoIP2Error
from django.core.handlers.wsgi import WSGIRequest
from DjangoWebsite.settings import GEOIP_DATABASE_FILE

geoip2 = GeoIP2(GEOIP_DATABASE_FILE)


def get_ip(request: WSGIRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[-1].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')


def get_city(request: WSGIRequest, default=None) -> Union[Tuple[int, Dict[str, str]], None]:
    try:
        ip = get_ip(request)
        return ip, geoip2.city(ip)
    except (GeoIP2Exception, GeoIP2Error):
        return default
