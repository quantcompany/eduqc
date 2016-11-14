from django import forms
from django.contrib.auth import authenticate
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


class ProfileForm(forms.ModelForm):
    old_password = forms.CharField(required=False, strip=False)
    new_password1 = forms.CharField(required=False, strip=False)
    new_password2 = forms.CharField(required=False, strip=False)
    change_password = forms.BooleanField(required=False)

    error_messages = {
        'authentication_failed': 'Clave incorrecta',
        'password_mismatch': 'Las claves no coinciden'
    }

    def clean(self):
        if self.cleaned_data.get('change_password'):
            assert hasattr(self, 'instance') and self.instance is not None
            user = self.instance
            pwd = self.cleaned_data.get('old_password')

            if not authenticate(username=user.email, password=pwd):
                raise forms.ValidationError(
                    {'old_password': self.error_messages['authentication_failed']},
                    code='authentication_failed',
                )


    def clean_new_password2(self):
        p1 = self.cleaned_data.get('new_password1')
        p2 = self.cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return p2


class StudentProfileForm(ProfileForm):
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


class InstructorProfileForm(ProfileForm):
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


class StaffProfileForm(ProfileForm):
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
