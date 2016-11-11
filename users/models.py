from django.db import models
from custom_user.models import AbstractEmailUser
from .choices import COUNTRY_CHOICES, GENDER_CHOICES


class EmailVerification(models.Model):
    user = models.ForeignKey('users.User', related_name='verifications')
    code = models.CharField(max_length=40, unique=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class User(AbstractEmailUser):
    """
    Users for the application
    """
    user_name = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True, choices=COUNTRY_CHOICES) # Add country list
    image = models.ImageField(upload_to='users/images', blank=True)

    DEFAULT_IMAGE_URL = '/static/images/teacher-1.png'

    def save(self, *args, **kwargs):
        self.guess_user_name()
        super(User, self).save(*args, **kwargs)

    def is_student(self):
        return hasattr(self, 'student')

    def is_instructor(self):
        return hasattr(self, 'instructor')

    def image_url(self):
        if self.image and self.image.name:
            return self.image.url
        else:
            return self.DEFAULT_IMAGE_URL

    def guess_user_name(self):
        if not self.user_name:
            if self.first_name or self.last_name:
                self.user_name = '{0} {0}'.format(self.first_name, self.last_name).strip()
            else:
                self.user_name = self.email.split('@')[0]
            # self.save()
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
    default_credentials = """<p>
        Para recibir tus clases, debes ingresar a <a href="#">www.wiziq.com/quantcompany</a> con las siguientes credenciales:
        <br/>
        Usuario: ########
        Password: ########
        <br/>
        </p>"""

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    wiziq_credentials = models.TextField(blank=True, default=default_credentials)

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'


class Instructor(User):
    categories = models.ManyToManyField('courses.Category', related_name='instructors')
    years_of_experience = models.IntegerField()

    class Meta:
        verbose_name = 'instructor'
        verbose_name_plural = 'instructors'
