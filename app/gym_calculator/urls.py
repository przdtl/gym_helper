from django.urls import path
from django.views.generic import TemplateView

from gym_calculator.views import BenchCalculatorView

app_name = 'calculator'

urlpatterns = [
    path('', BenchCalculatorView.as_view(), name='index'),
]
