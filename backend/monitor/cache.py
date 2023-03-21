import time
from .models import RequestAnalysis


class RequestCache(object):
    def __init__(self):
        self.request = 0
        self.created = time.time()

    def add(self):
        self.request += 1
        self.detect()

    def detect(self):
        if (time.time() - self.created) / 3600 / 24 >= 1.:
            self.save()

    def save(self):
        RequestAnalysis.objects.create(request=self.request)
        self.request = 0
        self.created = time.time()


requestCache = RequestCache()
