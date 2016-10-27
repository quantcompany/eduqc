from django.db import models


class Session(models.Model):
    course = models.ForeignKey('courses.Course', related_name='sessions')
    start_date = models.DateField()
    optional_text = models.TextField()  # para hacer alguna aclaracion sobre esta sesión
    instructor = models.ForeignKey('users.Instructor', related_name='sessions')
    students = models.ManyToManyField('users.Student', related_name='sessions', through='sesiones.Enrollment')


class Enrollment(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('cancelled', 'Cancelled'), ('finished', 'Finished')]

    session = models.ForeignKey('sesiones.Session', related_name='enrollments')
    student = models.ForeignKey('users.Student', related_name='enrollments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    transaction = models.CharField(max_length=100, default='0')

    class Meta:
        ordering = ['last_modified', 'enrollment_date']
