import re

from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, get_object_or_404

from .forms import CourseFilterForm
from .models import Course, Category


def index(request, *args, **kwargs):
    return render(request, 'courses/index.html', {'categories': Category.objects.all()})


def detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    if request.user.is_authenticated:
        if request.user.is_student() and request.user.student.enrollments.filter(course=course, status='active').exists():
            return render(request, 'courses/detail_private.html', {'course': course})
        else:
            return render(request, 'courses/detail_public.html', {'course': course})
    else:
        return render(request, 'courses/detail_public.html', {'course': course})


def course_filter(request):
    form = CourseFilterForm(request.POST)

    courses = Course.objects.all()

    if form.is_valid():
        categories = form.cleaned_data['categories']

        if len(categories) > 0:
            courses = courses.filter(category__in=categories)

        words = form.cleaned_data.get('query', '')
        words = words.strip()
        words = re.sub(r'  +', ' ', words).split(' ')

        sq = None
        if len(words) > 0:
            sq = SearchQuery(words[0])
            for word in words[1:]:
                sq = sq | SearchQuery(word)

        if sq is not None:
            sv = SearchVector('name', 'description')
            courses = courses.annotate(rank=SearchRank(sv, sq)).order_by('-rank')

    paginator = Paginator(courses, settings.COURSES_PER_PAGE)

    results = {
        'page_count': paginator.num_pages,
        'pages': []
    }

    for page_num in paginator.page_range:
        results['pages'].append({
            'number': page_num,
            'courses': [c.as_dict() for c in paginator.page(page_num)]
        })

    return JsonResponse(results)
