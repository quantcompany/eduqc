from django.shortcuts import render


from users.forms import SignUpForm


def index(request, *args, **kwargs):
    ctx = {
        'sign_up_form': SignUpForm()
    }
    return render(request, 'index/index.html', ctx)
