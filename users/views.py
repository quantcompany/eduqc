import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from emails import send_verification_email

from .models import EmailVerification
from .forms import SignUpForm


def signin(request):
    form = AuthenticationForm(request, data=request.POST)    # email = request.POST.get('email', None)

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


def verify(request, code):
    verification = get_object_or_404(EmailVerification, code=code)
    user = verification.user
    user.is_active = True
    user.save()
    return render(request, 'users/verified.html')
