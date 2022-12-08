import psutil
from timeloop import Timeloop
from datetime import timedelta

loop = Timeloop()


@loop.job(timedelta(seconds=1))
def monitor():
    psutil.cpu_percent()


loop.start()
