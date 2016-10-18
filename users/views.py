from django.http import JsonResponse
from django.shortcuts import render

from .forms import SignUpForm


def signin(request):
    pass


def signup(request):
    form = SignUpForm(request.POST)

    if form.is_valid():
        return JsonResponse({})
    else:
        return JsonResponse(form.errors, status=400)        
