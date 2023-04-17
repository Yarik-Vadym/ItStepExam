from .models import Blog
from django import forms
from django.forms import ModelForm


class BlogForm(ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'content', 'img_path']
        labels = {'title': 'Заголовок', 'content': 'Контент', 'img_path': 'Изображение'}
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'img_path': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
