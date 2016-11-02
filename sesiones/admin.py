from django.contrib import admin

from .models import Session, Enrollment


admin.site.register(Session)
admin.site.register(Enrollment)
