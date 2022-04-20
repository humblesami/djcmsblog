from django.utils.deprecation import MiddlewareMixin


class LayoutMiddleWare(MiddlewareMixin):
    def process_response(self, request, response):
        response['header_data'] = {}
        response['footer_data'] = {}
        return response