from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}))


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.pop('autofocus')

    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={"class": 'form-control'}))

    class Meta:
        model = get_user_model()  # связываем форму с моделью get_user_model() подвязывает кастомную модель
        fields = ['username', 'email', 'password1', 'password2']  # Поля которые отображаются на странице(по порядку)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise ValidationError('Такой email уже сущевствует')
        return email

    def clean_username(self):  # clean_НАЗВАНИЕ_ПОЛЯ_МОДЕЛИ
        username = self.cleaned_data['username']  # Получаем строку
        if not re.match(r'[a-zA-Z0-9-_]', username):  # проверка на то что бы 1 символ не был цифрой
            raise ValidationError('Имя пользователя может состоять из латиницы, цыфр, и специальных символов -,_')
        return username


class SearchMainPageForm(forms.Form):
    name_coin = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Search...',
        'type': 'search',
        'class': 'form-control form-control-dark text-bg-dark',
        'aria_label': 'Search'
    }))