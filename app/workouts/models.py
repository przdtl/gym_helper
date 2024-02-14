from django.conf import settings
from django.db import models
from django.urls import reverse

from exercises.models import ExercisesModel


class WorkoutTemplate(models.Model):
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    workout_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ['created_by', 'workout_name']

    def __str__(self):
        return self.workout_name

    def get_absolute_url(self):
        return reverse('workouts:get_template', args=[self.id])


class ExercisesInWorkoutTemplate(models.Model):
    workout_template = models.ForeignKey(to=WorkoutTemplate, on_delete=models.CASCADE)
    exercise = models.ForeignKey(to=ExercisesModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'Упражнение "{self.exercise.exercise_name}" шаблона {self.workout_template.workout_name}'


class ApproachExercisesInWorkoutTemplate(models.Model):
    exercise_in_workout_template = models.ForeignKey(to=ExercisesInWorkoutTemplate, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(default=0)
    number_of_repetitions = models.PositiveIntegerField(default=0)


class Workout(models.Model):
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    beginning_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    ending_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Тренировка проходившая с {self.beginning_datetime} до {self.ending_datetime}'

    def get_absolute_url(self):
        return reverse('workouts:get_training', args=[self.id])


class ExercisesInWorkout(models.Model):
    workout = models.ForeignKey(to=Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(to=ExercisesModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'Упражнение "{self.exercise.exercise_name}". {self.workout}'


class ApproachExercisesInWorkout(models.Model):
    exercise_in_workout = models.ForeignKey(to=ExercisesInWorkout, on_delete=models.CASCADE, blank=True, null=True)
    weight = models.PositiveIntegerField(default=0)
    number_of_repetitions = models.PositiveIntegerField(default=0)
    datetime = models.TimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.weight} кг на {self.number_of_repetitions}'
