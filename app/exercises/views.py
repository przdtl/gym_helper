from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from exercises.models import ExercisesModel, ExerciseCategoriesModel


class EntireExerciseListView(ListView):
    template_name = 'exercises/entire_exercises.html'
    model = ExercisesModel
    paginate_by = 15

    def get_queryset(self):
        return ExercisesModel.objects.all().order_by('exercise_name')


class ExerciseCategoriesListView(ListView):
    template_name = 'exercises/entire_categories.html'
    model = ExerciseCategoriesModel
    paginate_by = 15

    def get_queryset(self):
        return ExerciseCategoriesModel.objects.all()


class ExerciseListByCategoryView(ListView):
    template_name = 'exercises/entire_category.html'
    model = ExercisesModel
    paginate_by = 15

    def get_queryset(self):
        category_slug = self.kwargs['category_name']
        return ExercisesModel.objects.filter(category__slug=category_slug)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_slug = self.kwargs['category_name']
        context['category'] = ExerciseCategoriesModel.objects.get(slug=category_slug)
        return context


class ExerciseView(DetailView):
    template_name = 'exercises/exercise_page.html'
    model = ExercisesModel

    def get_object(self, queryset=None):
        category_slug = self.kwargs['category_name']
        exercise_slug = self.kwargs['exercise_name']
        return get_object_or_404(ExercisesModel, slug=exercise_slug, category__slug=category_slug)
