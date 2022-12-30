from typing import *
from typing import Union, Any

from django.utils import timezone
from .models import RequestAnalysis as model
from .cache import requestCache
import numpy


def analysis_request() -> List[int]:
    record = timezone.datetime.today().date()
    array = list(map(int, reversed([
        numpy.sum(
            model.objects.filter(date=record - timezone.timedelta(days=v)).values_list("request"),
            dtype=numpy.int
        )
        for v in range(7)
    ])))
    array[-1] += requestCache.request
    return array
