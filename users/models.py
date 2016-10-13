from django.db import models
from custom_user.models import AbstractEmailUser
from .choices import COUNTRY_CHOICES


class EmailVerification(models.Model):
    user = models.ForeignKey('users.User', related_name='verifications')
    code = models.CharField(max_length=40, unique=True)
    done = models.BooleanField(default=False)


class User(AbstractEmailUser):
    """
    Users for the application
    """
    user_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True, choices=COUNTRY_CHOICES) # Add country list

    def guess_user_name(self):
        if not self.user_name:
            if self.first_name or self.last_name:
                self.user_name = '{0} {0}'.format(self.first_name, self.last_name).strip()
            else:
                self.user_name = self.email.split('@')[0]

            self.save()
        return self.user_name

    def get_short_name(self):
        return self.user_name

    def get_full_name(self):
        return self.last_name + ", " + self.first_name

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'user_name': self.user_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'country': self.country
        }


class Student(User):
    pass

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'


class Instructor(User):
    categories = models.ManyToManyField('courses.Category', related_name='instructors')

    class Meta:
        verbose_name = 'instructor'
        verbose_name_plural = 'instructors'
