import sys
from django.core.paginator import Paginator, EmptyPage, Page
from django.db.models import QuerySet
from DjangoWebsite.settings import FILE_CACHE_CAPABILITY, FILE_PAGINATION
from typing import *
from functools import reduce

from files.models import UserFile


class FilePaginationCache(object):
    def __init__(self):
        self.capability = FILE_CACHE_CAPABILITY
        self.caches: Dict[str, Paginator] = {}
        self.queue: List[str] = []

    @property
    def length(self):
        return len(self.queue)

    def remove(self):
        del self.caches[self.queue.pop(0)]

    def removeAll(self):
        self.caches = {}
        self.queue = []

    def push(self, key, value):
        if self.length > self.capability:
            self.remove()
        self.caches[key] = value
        self.queue.append(key)

    def contains(self, key) -> bool:
        return key in self.queue

    def get(self, key, default=None):
        return self.caches.get(key, default)

    def get_page(self, key, page, default=None) -> Tuple[int, Page]:
        try:
            cache = self.caches[key]
            return cache.num_pages, cache.get_page(page)
        except (KeyError, EmptyPage):
            return default

    @staticmethod
    def search_keyword(keyword: str) -> QuerySet:
        return reduce(
            lambda _object, _keyword: _object.filter(real_name__icontains=_keyword),
            [UserFile.objects, *keyword.split(" ")],
        )

    def create(self, key, page) -> Tuple[int, Page]:
        file_objects = (self.search_keyword(key) if key else UserFile.objects).order_by("id")
        pagination = Paginator(file_objects, FILE_PAGINATION)
        self.push(key, pagination)
        return pagination.num_pages, pagination.get_page(page)

    def request(self, key, page, default=None) -> Tuple[int, Page]:
        if self.contains(key):
            return self.get_page(key, page, default)
        else:
            return self.create(key, page)

    @property
    def sys_size(self) -> int:
        return sys.getsizeof(self.queue) + sys.getsizeof(self.caches)

    __call__ = request


fileCache = FilePaginationCache()
