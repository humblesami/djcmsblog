from django.utils.deprecation import MiddlewareMixin

from website.models import Menu


class LayoutMiddleWare(MiddlewareMixin):
    
    def add_menu_to_response(self):
        additional = {}
        additional['header_data'] = {}
        additional['footer_data'] = {}
        main_menu = Menu.objects.filter(parent_id=None, name='main menu').first()
        if main_menu:
            child_menus = Menu.objects.filter(parent_id=main_menu.id, active=1)
            additional['child_menus'] = child_menus
        else:
            additional['child_menus'] = []
        additional['main_menu'] = main_menu
        return additional
    
    @classmethod
    def get_translations(cls):
        labels = {
            'footer': {
                'contact': {'0': 'Contact0', '1': 'Contact1'}
            },
            'contact_us': {
                'heading': 'Contact'
            }
        }
        return labels
    
    def process_template_response(self, request, response):
        req_path = request.path
        if not req_path.startswith('/admin'):
            additional = self.add_menu_to_response()
            response.context_data.update(additional)
            labels = self.__class__.get_translations()
            response.context_data.update(labels)
        return response
    
    def process_response(self, request, response):
        return response
