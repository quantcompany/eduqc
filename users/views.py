import itertools
import math
import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from emails import send_verification_email

from courses.models import Category

from .models import User, EmailVerification
from .forms import SignUpForm
from .choices import COUNTRY_CHOICES


def signin(request):
    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
        login(request, form.get_user())
        return JsonResponse({})
    else:
        return JsonResponse(form.errors, status=400)


def signup(request):
    form = SignUpForm(request.POST)

    if form.is_valid():
        new_student = form.save(commit=False)
        new_student.is_active = False
        new_student.save()

        code = str(uuid.uuid4())
        while EmailVerification.objects.filter(code=code).exists():
            code = str(uuid.uuid4())

        verification = new_student.verifications.create(code=code)
        send_verification_email(verification, site=get_current_site(request))

        return JsonResponse({})
    else:
        return JsonResponse(form.errors, status=400)


def signout(request):
    logout(request)
    return redirect(reverse('index'))


# @login_required
def verify(request, code):
    verification = get_object_or_404(EmailVerification, code=code)
    user = verification.user
    user.is_active = True
    user.save()
    return render(request, 'users/verified.html')


@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    ctx = dict()
    ctx['COUNTRY_CHOICES'] = COUNTRY_CHOICES

    category_cutoff = math.ceil(Category.objects.count() / 2)
    c1 = Category.objects.all()[:category_cutoff]
    c2 = Category.objects.all()[category_cutoff:]
    ctx['category_pairs'] = itertools.zip_longest(c1, c2)

    if profile_user.is_student():
        template = 'users/student_profile.html'
        ctx['profile_user'] = profile_user.student
    elif profile_user.is_instructor():
        template = 'users/instructor_profile.html'
        ctx['profile_user'] = profile_user.instructor

    return render(request, template, ctx)


@login_required
def me(request):
    return profile(request, request.user.id)
