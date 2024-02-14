from django.urls import path

from exercises.views import ExerciseView, EntireExerciseListView, ExerciseCategoriesListView, ExerciseListByCategoryView

app_name = 'exercises'

urlpatterns = [
    path('', EntireExerciseListView.as_view(), name='full_list'),
    path('categories/', ExerciseCategoriesListView.as_view(), name='categories'),
    path('categories/<slug:category_name>/', ExerciseListByCategoryView.as_view(), name='exercises_by_category'),
    path('categories/<slug:category_name>/<slug:exercise_name>/', ExerciseView.as_view(), name='get_exercise'),
]
