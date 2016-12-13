from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

########################################################
from django.utils.translation import ugettext_lazy as _
# esta funcion (ugettext_lazy) se usa para marcar traducciones en los models.
# se importa aqui con el alias "_" (un guion bajo) para que se pueda usar sin
# tener que escribir el nombre completo. Entonces, en lugar de esto:
# ugettext_lazy('Courses')
# se puede escribir esto:
# _('Courses')


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fa_icon = models.CharField(max_length=20, default='fa-graduation-cap')

    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Course(models.Model):
    LEVEL_CHOICES = [
        (1, _('Principiante')),
        (2, _('Intermediate')),
        (3, _('Advanced'))
    ]

    name = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=500)
    description = models.TextField()
    extended_description = models.TextField()
    duration = models.IntegerField()  # in weeks
    category = models.ForeignKey('courses.Category', related_name='courses')
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=100, unique=True)
    main_image = models.ImageField(upload_to='courses/images')
    details_document = models.FileField(upload_to='courses/pdf')
    level = models.IntegerField(choices=LEVEL_CHOICES)
    topics = models.TextField()
    audience = models.TextField()
    private_text = models.TextField()
    classes = models.IntegerField()
    mentorship_sessions = models.IntegerField()
    materials = models.TextField()
    projects = models.TextField()
    next_session = models.TextField()
    order = models.IntegerField() # Order used to order the courses 1 = first


    class Meta:
        ordering = ['name']
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subtitle': self.subtitle,
            'slug': self.slug,
            'description': self.description,
            'duration': self.duration,
            'category': self.category.as_dict(),
            'main_image': self.main_image.url,
        }

    def enroll(self, student, payment_id):
        self.enrollments.create(
            course=self,
            student=student,
            status='pending',
            total_price=self.monthly_price,
            payment_id=payment_id
        )


# class Document(models.Model):
#     course = models.ForeignKey('courses.Course', related_name='documents')
#     file = models.FileFiled()


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('active', _('Active')),
        ('cancelled', _('Cancelled')),
        ('finished', _('Finished')),
        ('refunded', _('Refunded')),
    ]

    course = models.ForeignKey('courses.Course', related_name='enrollments')
    student = models.ForeignKey('users.Student', related_name='enrollments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['-enrollment_date']
        verbose_name = _('enrollment')
        verbose_name_plural = _('enrollments')

    def __str__(self):
        return '{} ({}) - {}'.format(self.course, self.student, self.enrollment_date)


class FAQ(models.Model):
    question = models.CharField(max_length=400)
    answer = models.TextField()
    course = models.ForeignKey('courses.Course', related_name='faqs')

    class Meta:
        verbose_name = _('FAQs')
        verbose_name_plural = _('FAQs')


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    course = models.ForeignKey('courses.Course', related_name='reviews')
    user = models.ForeignKey('users.Student', related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
