from django.contrib import admin

from courses.models import Enrollment

from .models import EmailVerification, User, Student, Instructor


class EnrollmentInline(admin.TabularInline):
    fields = [
        'status',
        'course',
        'enrollment_date',
        'total_price',
        'payment_id',
    ]

    readonly_fields = [
        'course',
        'enrollment_date',
        'total_price',
        'payment_id',
    ]
    
    model = Enrollment

class StudentAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInline]

admin.site.register(EmailVerification)
admin.site.register(User)
admin.site.register(Student, StudentAdmin)
admin.site.register(Instructor)
