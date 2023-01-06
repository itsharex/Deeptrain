from time import time
from typing import Callable


def timeit_analysis(function: Callable[[any], any], count: int = 10 ** 6, *args, **kwargs):
    _current = time()
    for _ in range(count):
        function(*args, **kwargs)
    _cost = time() - _current
    return _cost


def fps_analysis(function: Callable[[any], any], count: int = 10 ** 5, *args, **kwargs):
    return 1 / timeit_analysis(function, count, *args, **kwargs) * count


def fps_compare(_function: callable, _comp_function: callable, count: int = 10 ** 5):
    fps = fps_analysis(_function, count)
    comp_fps = fps_analysis(_comp_function, count)

    return f"function fps: {fps}, compared function fps: {comp_fps}"
