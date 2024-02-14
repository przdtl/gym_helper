import re

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, FormView, UpdateView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from exercises.models import ExercisesModel, ExerciseCategoriesModel
from workouts.models import WorkoutTemplate, ExercisesInWorkoutTemplate, Workout, ExercisesInWorkout, \
    ApproachExercisesInWorkout
from workouts.forms import CreateNewWorkoutTemplateForm, ApproachExercisesInWorkoutForm


class WorkoutTemplatesView(MultipleObjectMixin, FormView):
    template_name = 'workouts/workout_templates.html'
    model = WorkoutTemplate
    form_class = CreateNewWorkoutTemplateForm
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user).order_by('id')

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['template_categories'] = dict()
        for template in self.get_queryset():
            context['template_categories'][template.id] = list(set(
                [exercise.exercise.category for exercise in
                 template.exercisesinworkouttemplate_set.all()]))
        context['unfinished_trainings'] = Workout.objects.filter(ending_datetime=None)
        return context

    def get_success_url(self):
        return reverse('workouts:get_template', args=[self.object.id])

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            data={'workout_name': request.POST['workout_name'], 'created_by': request.user})
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CreateWorkoutTemplatesView(CreateView):
    template_name = 'workouts/create_workout_template.html'
    model = WorkoutTemplate


class WorkoutTemplateDetailView(DetailView):
    template_name = 'workouts/get_workout_template.html'
    model = WorkoutTemplate


class DeleteExerciseFromWorkoutTemplateView(DeleteView):
    template_name = 'workouts/delete_exercise_from_template.html'
    model = ExercisesInWorkoutTemplate
    workout_id_of_exercise_deleted_from_template = None

    def get_success_url(self):
        return reverse('workouts:get_template', args=[self.workout_id_of_exercise_deleted_from_template])

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        self.workout_id_of_exercise_deleted_from_template = ExercisesInWorkoutTemplate.objects.get(
            id=object.id).workout_template.id
        object.delete()
        return redirect(self.get_success_url())


class DeleteWorkoutTemplateView(DeleteView):
    template_name = 'workouts/delete_workout_template.html'
    model = WorkoutTemplate

    def get_success_url(self):
        return reverse('workouts:templates')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return redirect(self.get_success_url())


class CreateWorkoutView(CreateView):
    template_name = 'workouts/create_workout.html'
    model = Workout
    workout = None

    def get_success_url(self):
        return reverse('workouts:get_training', args=[self.workout.id])

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        object = Workout(created_by=request.user)
        template_id = request.GET.get('template', None)
        object.save()
        if template_id is not None:
            exercises_in_template = WorkoutTemplate.objects.get(pk=template_id).exercisesinworkouttemplate_set.all()
            for exercise_in_template in exercises_in_template:
                object.exercisesinworkout_set.create(exercise=exercise_in_template.exercise)
                object.save()
        self.workout = self.model.objects.get(id=object.id)
        return redirect(self.get_success_url())


class WorkoutView(DetailView, FormMixin):
    template_name = 'workouts/get_workout.html'
    model = Workout
    form_class = ApproachExercisesInWorkoutForm

    def get_success_url(self):
        return reverse('workouts:get_training', args=[self.object.exercise_in_workout.workout.id])

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        exercise_in_workout = request.GET['exercise_in_workout_id']
        form = self.form_class(data={
            'weight': request.POST['weight'],
            'number_of_repetitions': request.POST['number_of_repetitions'],
            'exercise_in_workout': get_object_or_404(ExercisesInWorkout, id=int(exercise_in_workout))
        })
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteExerciseFromWorkoutView(DeleteView):
    template_name = 'workouts/delete_exercise_from_training.html'
    model = ExercisesInWorkout
    workout_id_of_exercise_deleted_from_training = None

    def get_success_url(self):
        return reverse('workouts:get_training', args=[self.workout_id_of_exercise_deleted_from_training])

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        self.workout_id_of_exercise_deleted_from_training = ExercisesInWorkout.objects.get(
            id=object.id).workout.id
        object.delete()
        return redirect(self.get_success_url())


class UpdateApproachExercisesInWorkout(SingleObjectMixin, FormView):
    template_name = 'workouts/update_approach.html'
    form_class = ApproachExercisesInWorkoutForm

    def get_success_url(self):
        return reverse('workouts:get_training', args=[self.object.exercise_in_workout.workout.id])

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        approach_id = kwargs.get('pk', None)
        approach = get_object_or_404(ApproachExercisesInWorkout, id=int(approach_id))
        form = self.form_class(instance=approach, data={
            'weight': request.POST['weight'],
            'number_of_repetitions': request.POST['number_of_repetitions'],
            'exercise_in_workout': approach.exercise_in_workout,
            'datetime': approach.datetime,
        })
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteApproachExercisesInWorkout(DeleteView):
    template_name = 'workouts/delete_approach_from_exercise.html'
    model = ApproachExercisesInWorkout
    workout_id_of_exercise_deleted_from_training = None

    def get_success_url(self):
        return reverse('workouts:get_training', args=[self.workout_id_of_exercise_deleted_from_training])

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        self.workout_id_of_exercise_deleted_from_training = self.model.objects.get(
            id=object.id).exercise_in_workout.workout.id
        object.delete()
        return redirect(self.get_success_url())


class StopWorkout(TemplateView):
    template_name = 'workouts/stop_workout.html'

    def get(self, request, *args, **kwargs):
        return self.post()

    def post(self):
        workout_id = self.kwargs.get('pk', None)
        workout = get_object_or_404(Workout, pk=workout_id)
        workout.ending_datetime = now()
        for exercise in workout.exercisesinworkout_set.all():
            if not exercise.approachexercisesinworkout_set.all().exists():
                exercise.delete()
        workout.save()
        return redirect(reverse('workouts:get_training', args=[workout.id]))


class AddExerciseToTemplate(TemplateView, MultipleObjectMixin):
    template_name = 'workouts/choose_exercises.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return ExerciseCategoriesModel.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        template_id = kwargs.get('pk')
        for key, value in request.POST.items():
            if re.match(r'checkbox_(\d+)', key):
                exercise_id = int(re.search(r'checkbox_(\d+)', key).group(1))
                get_object_or_404(WorkoutTemplate, id=int(template_id)).exercisesinworkouttemplate_set.create(
                    exercise_id=exercise_id)
        return HttpResponseRedirect(reverse('workouts:get_template', args=[template_id]))


class AddExerciseToWorkout(TemplateView, MultipleObjectMixin):
    template_name = 'workouts/choose_exercises.html'

    def get_queryset(self):
        return ExerciseCategoriesModel.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        workout_id = kwargs.get('pk')
        for key, value in request.POST.items():
            if re.match(r'checkbox_(\d+)', key):
                exercise_id = int(re.search(r'checkbox_(\d+)', key).group(1))
                get_object_or_404(Workout, id=int(workout_id)).exercisesinworkout_set.create(
                    exercise_id=exercise_id)
        return HttpResponseRedirect(reverse('workouts:get_training', args=[workout_id]))
