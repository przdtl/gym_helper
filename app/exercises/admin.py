from django.contrib import admin

from exercises.models import ExercisesModel, ExerciseCategoriesModel


@admin.register(ExercisesModel)
class ExercisesModelAdmin(admin.ModelAdmin):
    exclude = ['slug']


@admin.register(ExerciseCategoriesModel)
class ExerciseCategoriesModelAdmin(admin.ModelAdmin):
    exclude = ['slug']
