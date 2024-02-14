from django.views.generic import TemplateView


class IndexTemplate(TemplateView):
    template_name = 'gym_helper/index.html'
