from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin
from DjangoWebsite.settings import CODING


class CodecMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(CodecMiddleware, self).__init__(*args, **kwargs)

    def process_request(self, request: WSGIRequest):
        request.encoding = CODING
