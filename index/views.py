from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from emails import send_contact_email

from .forms import ContactForm


def index(request, *args, **kwargs):
    return render(request, 'index/index.html')

def contact(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'index/contact.html')
    elif request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            send_contact_email(form.cleaned_data, site=get_current_site(request))
            return JsonResponse({})
        else:
            return JsonResponse(form.errors, status=400)
