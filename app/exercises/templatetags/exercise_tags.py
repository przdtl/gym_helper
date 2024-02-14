from django.template.defaulttags import register

from workouts.models import ExercisesInWorkout


# Workout model
@register.filter
def in_created_by(things, category):
    return things.filter(workout__created_by=category)


# Workout model
@register.filter
def in_exercise_in_workout(things, category):
    return things.filter(exercise_in_workout_id=category)


# Reverse workouts
@register.filter
def reverse_workouts(things):
    return things.order_by('-workout__beginning_datetime')


# Reverse workouts
@register.filter
def reverse_approaches(thing):
    return thing.order_by('-datetime')
