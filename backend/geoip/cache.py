import json
import time
from .geoip import *
import sys
from typing import *
from django.core.handlers.wsgi import WSGIRequest
from .models import IPRequestAnalysis
from Deeptrain.settings import GEOIP_RELEASE_INTERVAL


class CountryCache(object):
    def __init__(self):
        self._caches: Dict[str, int] = {}
        self._total = 0
        self._released_stamp = int(time.time())

    @property
    def length(self):
        return len(self._caches)

    @property
    def total_requests(self):
        return self._total

    @property
    def data(self) -> str:
        """
        :return: json data (str)
        """
        return json.dumps(self._caches)

    def clear(self):
        self._caches = {}
        self._total = 0
        self._released_stamp = int(time.time())

    def get(self, country, default=0):
        return self._caches.get(country, default)

    def add(self, country) -> None:
        self._total += 1
        if country in self._caches:
            self._caches[country] += 1
        else:
            self._caches[country] = 1

    def request(self, request: WSGIRequest) -> str:
        response = get_country_name_from_request(request)
        if response:
            self.detect_cache()
            self.add(response)
        return response or "Unknown"

    def ip(self, ip: str) -> str:
        response = get_country_name_from_ip(ip)
        if response:
            self.detect_cache()
            self.add(response)
        return response or "Unknown"

    def refresh(self) -> None:
        IPRequestAnalysis.objects.create(total=self.total_requests, json_countries=self.data)
        self.clear()

    def detect_cache(self) -> None:
        if time.time() - self._released_stamp >= GEOIP_RELEASE_INTERVAL:
            self.refresh()

    @property
    def sys_size(self) -> int:
        return sys.getsizeof(self._caches)

    def serialize(self) -> Tuple[int, str]:
        return self.total_requests, self.data

    __call__ = request


countryCache = CountryCache()
