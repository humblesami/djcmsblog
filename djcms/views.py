from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            return self.render_to_response(context)
        except Exception as e:
            message = str(e)
            context['error'] = message
            response = render(request, self.template_name, context)
            return response
