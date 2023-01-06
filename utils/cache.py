from django.core.cache import cache
from typing import *
import os

pid = os.getpid()
default_expiration = 60


def _hash_cache(expiration=default_expiration, version=None):
    """

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
