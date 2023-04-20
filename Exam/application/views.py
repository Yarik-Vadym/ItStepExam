from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework import generics, permissions
from binance.client import Client
from .serializers import MyModelSerializer
from .models import Coins
from .forms import UserRegisterForm, UserLoginForm, SearchMainPageForm
from .config import *


class CoinsListView(generics.ListCreateAPIView):
    queryset = Coins.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = (permissions.IsAdminUser,)


class CoinDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coins.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = (permissions.IsAdminUser,)


def divine_number(number_str: str, length: int = 0) -> str:
    left_side = f'{int(number_str.split(".")[0]):,}'
    if length >= 1:
        right_side = number_str.split(".")[1][:length]
        return f'{left_side}.{right_side}'
    return left_side


def home(request):
    client = Client(API_B, Secret_B)
    coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'BUSDUSDT', 'ADAUSDT', 'DOGEUSDT',
             'SOLUSDT', 'MATICUSDT', 'DOTUSDT']
    symbol_ticker = client.get_symbol_ticker()
    get_ticker = client.get_ticker()
    data = {}
    for j in coins:
        for i in symbol_ticker:
            if i['symbol'] == j:
                data[j] = i['price']
    coins_len = len(coins)
    for count in range(coins_len):
        for i in get_ticker:
            if i['symbol'] == coins[count]:
                name = coins[count]
                data[name] = {'price': '$ ' + divine_number(data[name], 3), 'full_name': name,
                                  'volume': divine_number(i['volume']), 'procent_change': divine_number(i['priceChangePercent'], 2) + ' %',
                                'quote_volume': divine_number(i['quoteVolume']), 'html_tag': {'price': name + 'price',
                                                                               'name': name + 'name',
                                  'volume': name + 'volume', 'procent_change': name + 'procent',
                                'quote_volume': name + 'quote'}}
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    if request.method == 'POST':
        form = SearchMainPageForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin'].upper()
            response = redirect('spot_coin')
            response.set_cookie('name', name_coin)
            response.set_cookie('is_first', False)
            return response
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = SearchMainPageForm()
    return render(request, 'application/index.html', {'coins': data, 'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                if form.cleaned_data['remember_me']:
                    request.session.set_expiry(14 * 24 * 60 * 60)  # Two weeks
                else:
                    request.session.set_expiry(0)  # When the browser closes
                return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'application/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # сохраняем форму
            login(request, user)  # сразу заходим в аккаунт
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'application/login.html', {'form': form})
