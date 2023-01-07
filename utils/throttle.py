from utils.cache import integer_operation
from django.core.cache import cache
from typing import *


def rate_throttle(key: Any, throttle: int, version=None, expiration=60, touch=False) -> bool:
    return integer_operation(key, expiration=expiration, version=version, touch=touch) > throttle


def _user_throttle(user, operate_type, times: int, expiration=60) -> bool:
    return rate_throttle(operate_type, times, version=user.id, expiration=expiration)


def not_serious_throttle(user, operate_type) -> bool:
    # 15秒操作8次 限流, 如点赞操作 (≈ 0.6 qps)
    return _user_throttle(user, operate_type, times=8, expiration=15)


def simple_throttle(user, operate_type) -> bool:
    # 一分钟内操作7次 限流, 如评论操作 (≈ 8.751s per query)
    return _user_throttle(user, operate_type, times=7, expiration=60)


def important_level_throttle(client, operate_type) -> int:
    # 分级请求限流, 如登录, 注册等重要操作
    """
    :param client: any
    :param operate_type: str
    :return: level
        - 0: means that the operation is permitted (query 8/m, );
        - 1: operation denied, level not serious - (wait 30s, 6 up);
        - 2: operation denied, serious level; (wait 240s, forever [, continuation]);
    """
    value = integer_operation(operate_type, expiration=60, version=client)
    if value <= 8:  # level 0
        return 0
    elif value <= 14:
        cache.touch(operate_type, 30, version=client)
        return 1
    else:
        cache.touch(operate_type, 240, version=client)
        return 2
