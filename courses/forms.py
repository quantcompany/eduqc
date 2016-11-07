from django import forms

from .models import Category


class CourseFilterForm(forms.Form):
    query = forms.CharField(required=False)
    categories = forms.ModelMultipleChoiceField(required=False, queryset=Category.objects.all())
