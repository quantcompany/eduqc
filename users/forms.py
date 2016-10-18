from django import forms 
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Student


class SignUpForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('email',)
        field_classes = {'email': UsernameField}

    def save(self, commit=True):
        student = super(UserCreationForm, self).save(commit=False)
        student.set_password(self.cleaned_data['password1'])
        if commit:
            student.save()
        return student