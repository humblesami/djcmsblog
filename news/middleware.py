from django.utils.deprecation import MiddlewareMixin
from user_agents import parse
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

    @classmethod
    def get_template(cls, ua_string):
        template = "website/two_columns.html"
        user_agent = parse(ua_string)
        if user_agent.is_mobile:
            template = "website/one_column.html"
        return template
    
    def process_template_response(self, request, response):
        req_path = request.path
        if not req_path.startswith('/admin'):
            additional = self.add_menu_to_response()
            additional['translations'] = self.__class__.get_translations()
            ua_string = request.META.get('HTTP_USER_AGENT')
            chosen_template = "website/two_columns.html"
            # chosen_template = self.__class__.get_template(ua_string)
            # if chosen_template.endswith('two_columns.html'):
            #     additional['left_col'] = {}
            #     additional['right_col'] = {}
            additional['chosen_template'] = chosen_template
            response.context_data.update(additional)
        return response
    
    def process_response(self, request, response):
        return response
