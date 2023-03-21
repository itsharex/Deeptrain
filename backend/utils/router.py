from rest_framework import routers
from typing import *

router = routers.DefaultRouter()


def register(path: str) -> Callable[[object], object]:
    def wrap(view: object):
        router.register(path, view)
        return view
    return wrap
