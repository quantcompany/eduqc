from django.contrib import admin

from .models import Course, Category


class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'category',
        'duration',
        'monthly_price',
        'level',
    ]

    list_filter = [
        'category',
        'level',
    ]

class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
