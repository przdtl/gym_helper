from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
import math

from gym_calculator.forms import BenchCalculatorForm


class BenchCalculatorView(FormView):
    template_name = 'calculator/bench_calculator.html'
    form_class = BenchCalculatorForm
    # success_url = reverse_lazy('calculator:index')
    plus_context = {}
    formulas = {
        'Формула Эпли': lambda M, k: (M * k) / 30 + M,
        'Формула Бжицки': lambda M, k: M * (36 / (37 - k)),
        'Формула Лэндера': lambda M, k: (100 * M) / (101.3 - 2.67123 * k),
        "Формула О'Коннора": lambda M, k: M * (1 + 0.025 * k),
        'Формула Ламбарди': lambda M, k: M * k ** 0.1,
        'Формула Мэйхью': lambda M, k: (100 * M) / (52.2 + 41.9 * math.exp((-0.055 * k))),
        'Формула Ватана': lambda M, k: (100 * M) / (48.8 + 53.8 * math.exp(-0.075 * k)),
    }

    def form_valid(self, form):
        M = float(form.cleaned_data['barbell_weight'])
        key = int(form.cleaned_data['reps'])
        d = dict(form.fields['reps'].choices)
        k = int(d[key])

        self.plus_context['formulas'] = dict()
        for key, value in self.formulas.items():
            self.plus_context['formulas'][key] = round(self.formulas[key](M, k), 2)

        self.plus_context['result'] = round(
            sum(map(float, self.plus_context['formulas'].values())) / len(self.plus_context['formulas']), 2)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in self.plus_context.items():
            context[key] = value
        self.plus_context.clear()

        if 'formulas' not in context:
            context['formulas'] = dict()
            for key, value in self.formulas.items():
                context['formulas'][key] = ''
            if context.get('result', None) is not None:
                del context['result']
        return context
