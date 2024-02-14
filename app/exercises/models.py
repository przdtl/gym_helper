from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class ExerciseCategoriesModel(models.Model):
    category_name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='exercise_category_images', null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)


class ExercisesModel(models.Model):
    exercise_name = models.CharField(max_length=255, null=False)
    category = models.ForeignKey(to=ExerciseCategoriesModel, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='exercise_images', null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        unique_together = ['exercise_name', 'category']

    def get_absolute_url(self):
        return reverse('exercises:get_exercise',
                       kwargs={'category_name': self.category.slug, 'exercise_name': self.slug})

    def instruction_as_list(self):
        return self.instruction.split(';')[:-1] if self.instruction else []

    def __str__(self):
        return f'{self.exercise_name} на {str(self.category).lower()}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.exercise_name)
        super().save(*args, **kwargs)
