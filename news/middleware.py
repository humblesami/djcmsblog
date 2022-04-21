from django.utils.deprecation import MiddlewareMixin

from website.models import Menu


class LayoutMiddleWare(MiddlewareMixin):
    
    def add_menu_to_response(self):
        additional = {}
        additional['header_data'] = {}
        additional['footer_data'] = {}
        main_menu = Menu.objects.filter(parent_id=None, name='main menu').first()
        child_menus = Menu.objects.filter(parent_id=main_menu.id, active=1)
    
        additional['child_menus'] = child_menus
        additional['main_menu'] = main_menu
        return additional
    
    def process_template_response(self, request, response):
        additional = self.add_menu_to_response()
        response.context_data.update(additional)
        return response
    
    def process_response(self, request, response):
        return response
