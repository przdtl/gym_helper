# Generated by Django 4.2.9 on 2024-02-14 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercises', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_name', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('created_by', 'workout_name')},
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginning_datetime', models.DateTimeField(auto_now_add=True)),
                ('ending_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExercisesInWorkoutTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.exercisesmodel')),
                ('workout_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.workouttemplate')),
            ],
        ),
        migrations.CreateModel(
            name='ExercisesInWorkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.exercisesmodel')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.workout')),
            ],
        ),
        migrations.CreateModel(
            name='ApproachExercisesInWorkoutTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField(default=0)),
                ('number_of_repetitions', models.PositiveIntegerField(default=0)),
                ('exercise_in_workout_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.exercisesinworkouttemplate')),
            ],
        ),
        migrations.CreateModel(
            name='ApproachExercisesInWorkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField(default=0)),
                ('number_of_repetitions', models.PositiveIntegerField(default=0)),
                ('datetime', models.TimeField(auto_now_add=True, null=True)),
                ('exercise_in_workout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workouts.exercisesinworkout')),
            ],
        ),
    ]
