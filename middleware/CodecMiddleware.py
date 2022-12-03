from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin
from DjangoWebsite.settings import CODING


class CodecMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(CodecMiddleware, self).__init__(*args, **kwargs)

    @staticmethod
    def process_request(request: WSGIRequest):
        request.encoding = CODING
