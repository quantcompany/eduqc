from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator

from.models import Course, Category


def index(request, *args, **kwargs):
    page_number = int(request.GET.get('p', '1'))
    category_filter = [int(id) for id in request.GET.getlist('c')]

    if len(category_filter) > 0:
        courses = Course.objects.filter(category__id__in=category_filter)
    else:
        courses = Course.objects.all()

    paginator = Paginator(courses, settings.COURSES_PER_PAGE)

    if page_number < 1 or page_number > paginator.num_pages:
        page_number = 1

    category_query = '&'.join(['c={0}'.format(c) for c in category_filter])

    context = {
        'page': paginator.page(page_number),
        'page_range': paginator.page_range,
        'categories': Category.objects.all(),
        'category_query': category_query
    }

    if request.is_ajax():
        return render(request, 'courses/includes/course_list.html', context)
    else:
        return render(request, 'courses/index.html', context)
