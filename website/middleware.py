from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .utils import get_session_timezone
from django.conf import settings
from django.http import HttpResponse


class LayoutMiddleWare(MiddlewareMixin):
    def process_response(self, request, response):
        response['header_data'] = {}
        response['footer_data'] = {}
        return response


class TimezoneMiddleware(MiddlewareMixin):

    def get_timezone_from_request(self, request):
        session = getattr(request, 'session', None)
        if session:
            res = get_session_timezone(session)
            return res

    def process_request(self, request):
        zone = self.get_timezone_from_request(request)
        if zone:
            timezone.activate(zone)


class CacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not response.get('Cache-Control') and not response.get('cache-control'):
            cache = f'public, max-age={180}'
            response['Cache-Control'] = cache
        return response


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            message = exception.args[1].replace("\'", '"')
            return HttpResponse(message)
