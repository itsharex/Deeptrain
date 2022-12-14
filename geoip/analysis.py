import json
from typing import *
from django.utils import timezone
from .models import IPRequestAnalysis
from .cache import countryCache
from functools import reduce
from operator import add


def sum_json_dictionary_cache(json_dicts: tuple) -> dict:
    dicts = tuple(map(json.loads, json_dicts))
    keys = set(reduce(add, map(lambda dic: tuple(dic.keys()), dicts)))
    return {
        key: sum([dic.get(key, 0) for dic in dicts])
        for key in keys
    }


def as_echarts_map(map_dict: Dict[str, int]) -> List[dict]:
    return [{"name": key, "value": value} for key, value in zip(map_dict.keys(), map_dict.values())]


def analysis_geoip() -> Tuple[int, List[dict]]:
    countryCache.detect_cache()
    begin_time = timezone.now() - timezone.timedelta(days=7)
    total_arrays, datas = tuple(zip(
        *[*[(obj.total, obj.json_countries)
            for obj in IPRequestAnalysis.objects.filter(time__gt=begin_time).all()],
          countryCache.serialize()]
    ))
    return sum(total_arrays), as_echarts_map(sum_json_dictionary_cache(datas))


if __name__ == "__main__":
    print(analysis_geoip())
