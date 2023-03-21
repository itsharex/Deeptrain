from typing import *
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from geoip2.errors import GeoIP2Error
from django.core.handlers.wsgi import WSGIRequest
from Deeptrain.settings import GEOIP_DATABASE_FILE

geoip2 = GeoIP2(GEOIP_DATABASE_FILE)

"""
e.g.
{
    'city': None,
    'continent_code': 'AS',
    'continent_name': 'Asia',
    'country_code': 'CN', 'country_name': 'China', 'dma_code': None, 'is_in_european_union': False,
    'latitude': 34.7732, 'longitude': 113.722, 'postal_code': None, 'region': None, 'time_zone': 'Asia/Shanghai'
}
"""


def get_ip(request: WSGIRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[-1].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')


def get_city_from_ip(ip: str, default=None) -> Union[Dict[str, str], None]:
    try:
        return geoip2.city(ip)
    except (GeoIP2Exception, GeoIP2Error):
        return default


def get_city_from_request(request: WSGIRequest, default=None) -> Union[Dict[str, str], None]:
    try:
        return geoip2.city(get_ip(request))
    except (GeoIP2Exception, GeoIP2Error):
        return default


def get_country_name_from_ip(ip: str, default=None) -> Union[str, None]:
    try:
        return geoip2.country_name(ip)
    except (GeoIP2Exception, GeoIP2Error):
        return default


def get_country_name_from_request(request: WSGIRequest, default=None) -> Union[str, None]:
    try:
        return geoip2.country_name(get_ip(request))
    except (GeoIP2Exception, GeoIP2Error):
        return default
