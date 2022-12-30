import json
from typing import *
from django.utils import timezone
from .models import IPRequestAnalysis
from .cache import countryCache
from functools import reduce
from operator import add
from user.models import User
from collections import Counter


def sum_json_dictionary_cache(json_dicts: tuple) -> dict:
    dicts = tuple(map(json.loads, json_dicts))
    keys = set(reduce(add, map(lambda dic: tuple(dic.keys()), dicts)))
    return {
        key: sum([dic.get(key, 0) for dic in dicts])
        for key in keys
    }


def as_echarts_map(map_dict: Dict[str, int]) -> List[dict]:
    return [{"name": key, "value": value} for key, value in zip(map_dict.keys(), map_dict.values())]


def analysis() -> Dict[str, any]:
    countryCache.detect_cache()
    begin_time = timezone.datetime.date(timezone.now()) - timezone.timedelta(days=6)
    total_arrays, datas = tuple(zip(
        *[*[(obj.total, obj.json_countries)
            for obj in IPRequestAnalysis.objects.filter(time__gt=begin_time).all()],
          countryCache.serialize()]
    ))
    total = User.objects.count()
    active = User.objects.filter(date_joined__gt=begin_time).count()
    admin = User.objects.filter(is_staff=True).count()

    countryVal = dict(Counter(map(lambda tup: str(tup[0]), User.objects.values_list("country"))))

    registers = []
    time_cursor = timezone.now()
    for _ in range(7):
        time_cursor -= timezone.timedelta(days=1)
        query = User.objects.filter(
            last_login__range=(
                time_cursor - timezone.timedelta(days=1), time_cursor,
            )
        )
        registers.append(query.count())

    return {
        "total": sum(total_arrays),
        "data": as_echarts_map(sum_json_dictionary_cache(datas)),
        "registered": total,
        "actives": active,
        "admin": admin,
        "userData": as_echarts_map(countryVal),
        "registeredData": list(reversed(registers)),
    }


if __name__ == "__main__":
    print(analysis())
