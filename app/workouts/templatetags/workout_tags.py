from django import template

from django.template.defaulttags import register
from workouts.models import ApproachExercisesInWorkout


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_approach(pk, attr):
    obj = getattr(ApproachExercisesInWorkout.objects.get(id=pk), attr)
    return obj
