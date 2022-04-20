from django.utils.deprecation import MiddlewareMixin


class LayoutMiddleWare(MiddlewareMixin):
    def process_response(self, request, response):
        path = str(request.path)
        if path[-1:] == '/':
            path = path[:-1]
        is_file = False
        if path.startswith('/static'):
            is_file = True
        elif path.startswith('/media'):
            is_file = True
        else:
            if path.endswith(('.ico', '.js', '.manifest', '.json')):
                is_file = True
        if not is_file:
            response['header_data'] = {}
            response['footer_data'] = {}
        return response
