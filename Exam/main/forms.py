from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    first_name = forms.CharField(label="Апи ключ", widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label="Секретный ключ", widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя:", widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={"class": 'form-control'}))


class NameCoinForm(forms.Form):
    CHOICES = (('All', 'All'), ('Filled', 'Filled'), ('Canceled', 'Canceled'))
    name_coin = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Name coin",
        'size': "20",
        'style': "border-radius: 4px;"}))
    choice_status = forms.ChoiceField(widget=forms.Select(attrs={
       'style': "border-radius: 4px;",
    }), choices=CHOICES)


class SearchCoinForm(forms.Form):
    name_coin = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Search',
        'type': 'text'
    }))


class BUYForm(forms.Form):
    def __init__(self, *args, **kwargs):
        initial_price = kwargs.pop('initial_price', None)
        super(BUYForm, self).__init__(*args, **kwargs)
        self.fields['price'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'buy-price',
            'name': 'buy-price',
            'value': initial_price
        }))
        self.fields['amount'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'buy-amount',
            'name': 'buy-amount'
        }))


class SELLForm(forms.Form):
    def __init__(self, *args, **kwargs):
        initial_price = kwargs.pop('initial_price', None)
        super(SELLForm, self).__init__(*args, **kwargs)
        self.fields['price'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'sell-price',
            'name': 'sell-price',
            'value': initial_price
        }))
        self.fields['amount'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'sell-amount',
            'name': 'sell-amount'
        }))


