from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from workouts.models import WorkoutTemplate, ApproachExercisesInWorkout


class CreateNewWorkoutTemplateForm(forms.ModelForm):
    workout_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-1', "autofocus": True}),
    )

    class Meta:
        model = WorkoutTemplate
        fields = ['workout_name', 'created_by']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'У вас уже существует тренировка с таким именем'
            }
        }


class ApproachExercisesInWorkoutForm(forms.ModelForm):
    weight = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-1'})
    )
    number_of_repetitions = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control mb-1'})
    )

    class Meta:
        model = ApproachExercisesInWorkout
        fields = ['weight', 'number_of_repetitions', 'exercise_in_workout']
