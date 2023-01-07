from django.core.cache import cache
from typing import *
from hashlib import md5, sha256
import os

pid = os.getpid()
default_expiration = 60


def clear():
    return cache.clear()


def _hash_cache(expiration=default_expiration, version=None):
    """
    Key Format: `:[version]:[hash]`

    :param version: cache version
    :param expiration: expiration seconds
    :return: decorator
    """

    def _decorate_(_exec_function: Callable[[Optional["Self"]], any]):
        """
        :param _exec_function:
            :param: self or None
            :return: picklable value
        :return: decorated function
        """
        _hash = hash(_exec_function)

        def _wrap_(*args, **kwargs):
            _cache = cache.get(_hash, version=version)
            if _cache is None:
                response = _exec_function(*args, **kwargs)
                cache.set(_hash, response, expiration, version=version)
                return response
            return _cache

        return _wrap_

    return _decorate_


def hash_cache_process_safe(param: Union[int, Callable[[Optional["Self"]], any]]):
    """
    :param param: expiration [int]
    :return: decorator

    or

    :param param: callable function [callable]
    :return: decorated function
    """
    if callable(param):
        return _hash_cache(version=pid)(param)
    else:
        return _hash_cache(param, version=pid)


class hash_cached_property:
    name = None

    def __init__(self, func, name=None, expiration=default_expiration):
        self.real_func = func
        self.__doc__ = getattr(func, '__doc__')
        self.expiration = expiration

    @staticmethod
    def _cls_hash_cache(_exec_function: Callable, expiration=default_expiration, version=None):
        def _wrap_(cls, *args, **kwargs):
            _hash = hash(cls)
            _cache = cache.get(_hash, version=version)
            if _cache is None:
                response = _exec_function(cls, *args, **kwargs)
                cache.set(_hash, response, expiration, version=version)
                return response
            return _cache

        return _wrap_

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
            self.func = self._cls_hash_cache(self.real_func, self.expiration, version=pid)
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same hash_cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in cache so that
        subsequent attribute during the period when the cache is not expire  (var: expiration)
        access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        return self if instance is None else self.func(instance)


def sha2_encode(text: str):
    """
    Return the 64-bit sha256 encoding value
    """

    return sha256(text.encode("utf-8")).hexdigest()


def md5_encode(text: str) -> str:
    """
    Return the 32-bit md5 encoding value
    """

    return md5(text.encode("utf-8")).hexdigest()


def short_md5_encode(text: str) -> str:
    """
    Return the 16-bit short md5 encoding value
    """

    return md5_encode(text)[8:-8]


def execute_or_get(key: Any, exec_, expiration=default_expiration, version=None,  *args, **kwargs):
    _cache = cache.get(key, version=version)
    if _cache is None:
        response = exec_(*args, **kwargs)
        cache.set(key, response, expiration, version=version)
        return response
    return _cache


def integer_operation(key: Any, delta: int = 1, default=1, expiration=default_expiration,
                      version=None, touch=False) -> int:
    try:
        ret = cache.incr(key, delta, version=version)
        if touch:
            cache.touch(key, expiration, version=version)
        return ret
    except (ValueError, TypeError):
        cache.set(key, default, expiration, version=version)
        return default


def times_limit(key: Any, max_limit, version=None, expiration=default_expiration, touch=False):
    return integer_operation(key, expiration=expiration, version=version, touch=touch) > max_limit
