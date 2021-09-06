from django import forms
from .models import Blog, BlogExplanation


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'img', 'description']


class BlogExplanationForm(forms.ModelForm):
    class Meta:
        model = BlogExplanation
        fields = ['img', 'caption']


class SearchForm(forms.Form):
    title = forms.CharField(max_length=100)

