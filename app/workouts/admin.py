from django.contrib import admin

from workouts.models import WorkoutTemplate, ExercisesInWorkoutTemplate, ApproachExercisesInWorkoutTemplate, Workout, \
    ExercisesInWorkout, ApproachExercisesInWorkout


@admin.register(WorkoutTemplate)
class WorkoutTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(ExercisesInWorkoutTemplate)
class ExercisesInWorkoutTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(ApproachExercisesInWorkoutTemplate)
class ApproachExercisesInWorkoutTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    pass


@admin.register(ExercisesInWorkout)
class ExercisesInWorkoutAdmin(admin.ModelAdmin):
    pass


@admin.register(ApproachExercisesInWorkout)
class ApproachExercisesInWorkoutAdmin(admin.ModelAdmin):
    pass
