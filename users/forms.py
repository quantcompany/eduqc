from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Student, Instructor, User


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


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'user_name',
            'first_name',
            'last_name',
            'description',
            'country',
            'image',
        )


class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = (
            'user_name',
            'first_name',
            'last_name',
            'description',
            'country',
            'image',
            'categories',
            'years_of_experience',
        )


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'user_name',
            'first_name',
            'last_name',
            'description',
            'country',
            'image',
        )
