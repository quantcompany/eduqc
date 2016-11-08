import re
import json
from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import requests
from .forms import CourseFilterForm
from .models import Course, Category


def index(request, *args, **kwargs):
    return render(request, 'courses/index.html', {'categories': Category.objects.all()})


def detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/detail_private.html', {'course': course})


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


def get_token():
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic QWFoNVlXVDBzS25uMndIZXNad0xQUV9TSGpGQUJ3X2lob1pfczlkcFV5SlczNlF6NmNaZkl4a0dlZW96WHpCcHZ5b0tYRE8tMk10WmxwSG06RUZ0ZzhVSmN3Z0VzejN0Qm1leW5lQmVydEtNTGxMaG1BZFJqTkotSzJUekNEQng1WTJMNl9LRGNIWHF0YVZiTTVMUkRrVGF1QTNpbXM2QVU='
    }
    payload = {'grant_type':'client_credentials'}
    r = requests.post(url, headers=headers, data=payload)
    print(r)
    print(r.json())
    return r.json()['access_token']


def checkout(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    url = 'https://api.sandbox.paypal.com/v1/payments/payment'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_token()
    }
    payload = {
        "intent": "sale",
 #       "experience_profile_id": "experience_profile_id",
        "redirect_urls":
            {
                "return_url": "http://return-url",
                "cancel_url": "http://cancel-url"
            },
        "payer":
            {
                "payment_method": "paypal"
            },
        "transactions": [
            {
                "amount":
                    {
                        "total": "4.00",
                        "currency": "USD",
                        "details":
                            {
                                "subtotal": "2.00",
                                "shipping": "1.00",
                                "tax": "2.00",
                                "shipping_discount": "-1.00"
                            }
                    },
                "item_list":
                    {
                        "items": [
                            {
                                "quantity": "1",
                                "name": "item 1",
                                "price": "1",
                                "currency": "USD",
                                "description": "item 1 description",
                                "tax": "1"
                            },
                            {
                                "quantity": "1",
                                "name": "item 2",
                                "price": "1",
                                "currency": "USD",
                                "description": "item 2 description",
                                "tax": "1"
                            }]
                    },
                "description": "The payment transaction description.",
                "invoice_number": "merchant invoice",
                "custom": "merchant custom data"
            }]
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    print(r)
    print(r.json())
    for link in r.json()['links']:
        if link['rel'] == 'approval_url':
            return HttpResponseRedirect(redirect_to=link['href'])

    return HttpResponse('Approval Failed')

"""
curl -v https://api.sandbox.paypal.com/v1/payments/payment \\
  -H 'Content-Type: application/json' \\
  -H 'Authorization: Bearer Access-Token' \\
  -d '{
  "intent": "sale",
  "experience_profile_id":"experience_profile_id",
  "redirect_urls":
  {
    "return_url": "http://return-url",
    "cancel_url": "http://cancel-url"
  },
  "payer":
  {
    "payment_method": "paypal"
  },
  "transactions": [
  {
    "amount":
    {
      "total": "4.00",
      "currency": "USD",
      "details":
      {
        "subtotal": "2.00",
        "shipping": "1.00",
        "tax": "2.00",
        "shipping_discount": "-1.00"
      }
    },
    "item_list":
    {
      "items": [
      {
        "quantity": "1",
        "name": "item 1",
        "price": "1",
        "currency": "USD",
        "description": "item 1 description",
        "tax": "1"
      },
      {
        "quantity": "1",
        "name": "item 2",
        "price": "1",
        "currency": "USD",
        "description": "item 2 description",
        "tax": "1"
      }]
    },
    "description": "The payment transaction description.",
    "invoice_number": "merchant invoice",
    "custom": "merchant custom data"
  }]
}'
"""