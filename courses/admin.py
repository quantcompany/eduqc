from django.contrib import admin

from .models import Course, Category, Enrollment


class CourseAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'slug',
        'subtitle',
        'order',
        'description',
        'extended_description',
        'duration',
        'category',
        'monthly_price',
        'main_image',
        'details_document',
        'level',
        'topics',
        'audience',
        'classes',
        'mentorship_sessions',
        'materials',
        'projects',
        'next_session',
        'private_text',
    ]

    list_display = [
        'name',
        'slug',
        'category',
        'duration',
        'monthly_price',
        'level',
    ]

    list_filter = [
        'category',
        'level',
    ]

    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Enrollment)
