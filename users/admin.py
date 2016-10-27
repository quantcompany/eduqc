from django.contrib import admin

from .models import EmailVerification, User, Student, Instructor


admin.site.register(EmailVerification)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
