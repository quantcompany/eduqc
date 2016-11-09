from datetime import timedelta

from django.db import models


class Session(models.Model):
    course = models.ForeignKey('courses.Course', related_name='sessions')
    start_date = models.DateField()
    optional_text = models.TextField()  # para hacer alguna aclaracion sobre esta sesión
    instructor = models.ForeignKey('users.Instructor', related_name='sessions')
    students = models.ManyToManyField('users.Student', related_name='sessions', through='sesiones.Enrollment')

    def __str__(self):
        return '{} ({})'.format(self.course, self.instructor)

    def enroll(self, student, payment_id):
        print('type of payment_id:')
        print(type(payment_id))
        self.enrollments.create(
            session=self,
            student=student,
            status='pending',
            total_price=self.course.monthly_price,
            payment_id=payment_id
        )

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.course.duration * 7)


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('finished', 'Finished')
    ]

    session = models.ForeignKey('sesiones.Session', related_name='enrollments')
    student = models.ForeignKey('users.Student', related_name='enrollments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['last_modified', 'enrollment_date']

    def __str__(self):
        return '{} ({})'.format(self.session, self.student)
