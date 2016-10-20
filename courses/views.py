from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .forms import CourseFilterForm
from .models import Course, Category


def index(request, *args, **kwargs):
    return render(request, 'courses/index.html', {'categories': Category.objects.all()})


def detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/detail.html', {'course': course})


def course_filter(request):
    form = CourseFilterForm(request.POST)

    courses = Course.objects.all()

    if form.is_valid():
        categories = form.cleaned_data['categories']
        if len(categories) > 0:
            courses = courses.filter(category__in=categories)

    paginator = Paginator(courses, settings.COURSES_PER_PAGE)

    results = {
        'page_count': paginator.num_pages,
        'pages': []
    }

    for page_num in paginator.page_range:
        results['pages'].append({'number': page_num, 'courses': [c.as_dict() for c in paginator.page(page_num)]})

    return JsonResponse(results)
