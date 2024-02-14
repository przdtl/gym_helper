from django.contrib.auth.decorators import login_required
from django.urls.conf import path, include

from workouts.views import WorkoutTemplatesView, CreateWorkoutTemplatesView, WorkoutTemplateDetailView, \
    DeleteExerciseFromWorkoutTemplateView, DeleteWorkoutTemplateView, WorkoutView, CreateWorkoutView, \
    DeleteExerciseFromWorkoutView, UpdateApproachExercisesInWorkout, DeleteApproachExercisesInWorkout, StopWorkout, \
    AddExerciseToTemplate, AddExerciseToWorkout

app_name = 'workouts'

templates_urlpatterns = [
    path('', login_required(WorkoutTemplatesView.as_view()), name='templates'),
    path('create_template/', login_required(CreateWorkoutTemplatesView.as_view()), name='create_template'),
    path('<int:pk>/', login_required(WorkoutTemplateDetailView.as_view()), name='get_template'),
    path('delete_exercise/<int:pk>/', login_required(DeleteExerciseFromWorkoutTemplateView.as_view()),
         name='delete_exercise_from_template'),
    path('delete_template/<int:pk>/', login_required(DeleteWorkoutTemplateView.as_view()),
         name='delete_template'),
    path('<int:pk>/add_exercise/', login_required(AddExerciseToTemplate.as_view()), name='add_exercise_to_template'),
]

workouts_urlpatterns = [
    path('<int:pk>/', login_required(WorkoutView.as_view()), name='get_training'),
    path('create_training/', login_required(CreateWorkoutView.as_view()), name='create_training'),
    path('delete_exercise/<int:pk>/', login_required(DeleteExerciseFromWorkoutView.as_view()),
         name='delete_exercise_from_training'),
    path('delete_approach/<int:pk>/', login_required(DeleteApproachExercisesInWorkout.as_view()),
         name='delete_approach_from_exercise'),
    path('update_exercise/<int:pk>/', login_required(UpdateApproachExercisesInWorkout.as_view()),
         name='update_exercise'),
    path('stop_workout/<int:pk>/', login_required(StopWorkout.as_view()), name='stop_workout'),
    path('<int:pk>/add_exercise/', login_required(AddExerciseToWorkout.as_view()), name='add_exercise_to_workout'),
]

urlpatterns = [
    path('templates/', include(templates_urlpatterns)),
    path('workout/', include(workouts_urlpatterns)),
]
