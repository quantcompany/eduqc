from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fa_icon = models.CharField(max_length=20, default='fa-graduation-cap')

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Course(models.Model):
    LEVEL_CHOICES = [(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')]

    name = models.CharField(max_length=300)
    description = models.TextField()
    duration = models.IntegerField() # in weeks
    category = models.ForeignKey('courses.Category', related_name='courses')
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    main_image = models.ImageField(upload_to='courses/images')
    level = models.IntegerField(choices=LEVEL_CHOICES)
    topics = models.TextField()
    audience = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'category': self.category.as_dict(),
            'main_image': self.main_image.url,
        }


class FAQ(models.Model):
    question = models.CharField(max_length=400)
    answer = models.TextField()
    course = models.ForeignKey('courses.Course', related_name='faqs')


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    course = models.ForeignKey('courses.Course', related_name='reviews')
    user = models.ForeignKey('users.Student', related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
