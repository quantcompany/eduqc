from django.http import JsonResponse
from django.shortcuts import render


def index(request, *args, **kwargs):
    return render(request, 'index/index.html')

def contact(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'index/contact.html')
    elif request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # form.save()
            # aqui se tiene que enviar el correo!
            return JsonResponse({})
        else:
            return JsonResponse(form.errors, status=400)
