from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

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
        form.save()
        return JsonResponse({})
    else:
        return JsonResponse(form.errors, status=400)        
