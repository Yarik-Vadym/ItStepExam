from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, NameCoinForm, SearchCoinForm, BUYForm, SELLForm
from .models import FilterModel
from binance.client import Client
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.http import JsonResponse


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            api_key = form.cleaned_data['first_name']
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Такая почта уже существует!')
            elif User.objects.filter(first_name__iexact=api_key).exists():
                messages.error(request, 'Такой апи ключ уже существует!')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                activateEmail(request, user, form.cleaned_data.get('email'))
                return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'sign_up.html', {'form': form})


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Дорогой {user}, пожалуйста перейдите на вашу электронную почту {to_email} входящие и нажмите \
             получена ссылка активации для подтверждения и завершения регистрации. Примечание: Посмотрите папку спам.')
    else:
        messages.error(request,
                       f'Проблема с отправкой письма с подтверждением на {to_email}, посмотрите всели вы написали коректно.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Спасибо за ваше подтверждение почты. Сейчас можете зайти в свой аккаунт.')
        return redirect('signin')
    else:
        messages.error(request, 'Ссылка не коректна!')

    return redirect('home')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'sing_in.html', {'form': form})


def account(request):
    your_models = User.objects.get(username=request.user.username)
    api_key = your_models.first_name
    secret_key = your_models.last_name
    client = Client(api_key, secret_key)
    info = client.get_account().get('balances')
    data = {'get_symbol_ticker': client.get_symbol_ticker(), 'get_ticker': client.get_ticker()}
    name_coins = []
    col_vo_coins = []
    price = []
    changes = []
    summa = []
    for i in info:
        if float(i.get('free')) > 0:
            free = float(i.get('free'))
            name_coins.append(i.get('asset'))
            col_vo_coins.append(float(i.get('free')))
            coin = i.get('asset')
            if coin == 'USDT':
                for i in data['get_symbol_ticker']:
                    if i['symbol'] == 'USDTUAH':
                        summa.append(free)
                        cost = round(float(i['price']) / 40, 2)
                        price.append(str(cost) + ' $')
                for i in data['get_ticker']:
                    if i['symbol'] == 'USDTUAH':
                        change = round(float(i['priceChangePercent']), 2)
                        if change > 0:
                            changes.append(change)
                        else:
                            changes.append(change)
            elif coin == 'UAH':
                for i in data['get_symbol_ticker']:
                    if i['symbol'] == 'USDTUAH':
                        summa.append(free / 40)
                        cost = round(float(i['price']), 2)
                        price.append(str(cost) + ' ₴')
                for i in data['get_ticker']:
                    if i['symbol'] == 'USDTUAH':
                        change = round(float(i['priceChangePercent']), 2)
                        if change > 0:
                            changes.append(change)
                        else:
                            changes.append(change)
            elif coin == 'LUNC':
                for i in data['get_symbol_ticker']:
                    if i['symbol'] == 'LUNCBUSD':
                        cost2 = float(i['price'])
                        summa.append(cost2 * free)
                        cost = float(i['price'])
                        price.append(str(cost) + ' $')
                for i in data['get_ticker']:
                    if i['symbol'] == 'LUNCBUSD':
                        change = round(float(i['priceChangePercent']), 2)
                        if change > 0:
                            changes.append(change)
                        else:
                            changes.append(change)
            else:
                for i in data['get_symbol_ticker']:
                    if i['symbol'] == coin + 'USDT':
                        cost2 = float(i['price'])
                        summa.append(cost2 * free)
                        cost = round(float(i['price']), 2)
                        price.append(str(cost) + ' $')
                for i in data['get_ticker']:
                    if i['symbol'] == coin + 'USDT':
                        change = round(float(i['priceChangePercent']), 2)
                        if change > 0:
                            changes.append(change)
                        else:
                            changes.append(change)
    sum_in_usdt = round(sum(summa), 2)
    for i in data['get_symbol_ticker']:
        if i['symbol'] == 'BTCUSDT':
            sum_in_btc = round(sum_in_usdt / float(i['price']), 9)
            return render(request, 'your_accaunt.html',
                          {'name_coin': name_coins, 'col_vo_coin': col_vo_coins, 'price': price, 'changes': changes,
                           'sum_in_usdt': sum_in_usdt, 'sum_in_btc': sum_in_btc})


def name_coin(request):
    if request.method == 'POST':
        form = NameCoinForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin'].upper()
            choice_status = form.cleaned_data['choice_status']
            FilterModel.objects.create(name_coin=name_coin, choice_status=choice_status)
            return redirect('history_spot')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = NameCoinForm()
    return render(request, 'enter_name_coin.html', {'form': form})


def history_spot(request):
    if request.method == 'POST':
        form = NameCoinForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin'].upper()
            choice_status = form.cleaned_data['choice_status']
            FilterModel.objects.create(name_coin=name_coin, choice_status=choice_status)
            return redirect('history_spot')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = NameCoinForm()
    your_models = User.objects.get(username=request.user.username)
    api_key = your_models.first_name
    secret_key = your_models.last_name
    client = Client(api_key, secret_key)
    all = FilterModel.objects.all()
    info = []
    inf = client.get_all_orders(symbol=all.last().name_coin)
    if all.last().choice_status == 'All':
        for j in inf:
            info.append(j)
    elif all.last().choice_status == 'Filled':
        for j in inf:
            if j['status'] == 'FILLED':
                info.append(j)
    elif all.last().choice_status == 'Canceled':
        for j in inf:
            if j['status'] == 'CANCELED':
                info.append(j)
    return render(request, 'history_spot.html', {'info': info, 'form': form})


def divine_number(number_str: str, length: int = 0) -> str:
    left_side = f'{int(number_str.split(".")[0]):,}'
    if length >= 1:
        right_side = number_str.split(".")[1][:length]
        return f'{left_side}.{right_side}'
    return left_side


def get_price_change(request):
    your_models = User.objects.get(username=request.user.username)
    api_key = your_models.first_name
    secret_key = your_models.last_name
    client = Client(api_key, secret_key)
    is_first = True if request.COOKIES['is_first'] == 'True' else False
    if not is_first:
        info = client.get_ticker(symbol=request.COOKIES['name'])
        data = {
            'price': divine_number(info['lastPrice'], 4),
            'change': round(float(info['priceChangePercent']), 2),
        }
    else:
        info = client.get_ticker(symbol='BTCUSDT')
        data = {
            'price': divine_number(info['lastPrice'], 4),
            'change': round(float(info['priceChangePercent']), 2),
        }
    return JsonResponse(data)


def spot(request):
    name = 'BTCUSDT'
    if request.method == 'POST':
        form = SearchCoinForm(request.POST)
        buy_form = BUYForm(request.POST)
        sell_form = SELLForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin'].upper()
            response = redirect('spot_coin')
            response.set_cookie('name', name_coin)
            response.set_cookie('is_first', False)
            return response
        elif buy_form.is_valid():
            your_models = User.objects.get(username=request.user.username)
            api_key = your_models.first_name
            secret_key = your_models.last_name
            client = Client(api_key, secret_key)
            buy_limit = client.create_order(
                symbol=name,
                side='BUY',
                type='LIMIT',
                timeInForce='GTC',
                quantity=buy_form.cleaned_data['amount'],
                price=buy_form.cleaned_data['price'])
            print(buy_limit)
            return redirect('account')
        elif sell_form.is_valid():
            print(1)
            your_models = User.objects.get(username=request.user.username)
            api_key = your_models.first_name
            secret_key = your_models.last_name
            client = Client(api_key, secret_key)
            sell_limit = client.create_order(
                symbol=name,
                side='SELL',
                type='LIMIT',
                timeInForce='GTC',
                quantity=sell_form.cleaned_data['amount'],
                price=sell_form.cleaned_data['price'])
            print(sell_limit)
            return redirect('account')
        else:
            for error in list(sell_form.errors.values()):
                messages.error(request, error)
    else:
        your_models = User.objects.get(username=request.user.username)
        api_key = your_models.first_name
        secret_key = your_models.last_name
        client = Client(api_key, secret_key)
        info = client.get_ticker(symbol=name)
        buy_form = BUYForm(initial_price=info['lastPrice'])
        sell_form = SELLForm(initial_price=info['lastPrice'])
        form = SearchCoinForm()
    your_models = User.objects.get(username=request.user.username)
    api_key = your_models.first_name
    secret_key = your_models.last_name
    client = Client(api_key, secret_key)
    info = client.get_ticker(symbol=name)
    asset = client.get_symbol_info(symbol=name)
    asset_balance_currency = client.get_asset_balance(asset=asset['quoteAsset'])
    asset_balance_coin = client.get_asset_balance(asset=asset['baseAsset'])
    responce = render(request, 'spot_trade.html', {'symbol': info['symbol'], 'price': divine_number(info['lastPrice'], 4),
                                               'change': round(float(info['priceChangePercent']), 2),
                                               'asset': asset['baseAsset'], 'form': form,
                                               'currency': asset['quoteAsset'],
                                               'asset_balance_currency': asset_balance_currency['free'],
                                               'asset_balance_coin': asset_balance_coin['free'], 'buy_form': buy_form, 'sell_form': sell_form})
    responce.set_cookie('is_first', True)
    return responce


def spot_coin(request):
    if request.method == 'POST':
        form = SearchCoinForm(request.POST)
        buy_form = BUYForm(request.POST)
        sell_form = SELLForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin'].upper()
            response = redirect('spot_coin')
            response.set_cookie('name', name_coin)
            response.set_cookie('is_first', False)
            return response
        elif buy_form.is_valid():
            your_models = User.objects.get(username=request.user.username)
            api_key = your_models.first_name
            secret_key = your_models.last_name
            client = Client(api_key, secret_key)
            buy_limit = client.create_order(
                symbol=request.COOKIES['name'],
                side='BUY',
                type='LIMIT',
                timeInForce='GTC',
                quantity=buy_form.cleaned_data['amount'],
                price=buy_form.cleaned_data['price'])
            print(buy_limit)
            return redirect('account')
        elif sell_form.is_valid():
            your_models = User.objects.get(username=request.user.username)
            api_key = your_models.first_name
            secret_key = your_models.last_name
            client = Client(api_key, secret_key)
            sell_limit = client.create_order(
                symbol=request.COOKIES['name'],
                side='SELL',
                type='LIMIT',
                timeInForce='GTC',
                quantity=sell_form.cleaned_data['amount'],
                price=sell_form.cleaned_data['price'])
            print(sell_limit)
            return redirect('account')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        your_models = User.objects.get(username=request.user.username)
        api_key = your_models.first_name
        secret_key = your_models.last_name
        client = Client(api_key, secret_key)
        info = client.get_ticker(symbol=request.COOKIES['name'])
        buy_form = BUYForm(initial_price=info['lastPrice'])
        sell_form = SELLForm(initial_price=info['lastPrice'])
        form = SearchCoinForm()
    your_models = User.objects.get(username=request.user.username)
    api_key = your_models.first_name
    secret_key = your_models.last_name
    client = Client(api_key, secret_key)
    info = client.get_ticker(symbol=request.COOKIES['name'])
    asset = client.get_symbol_info(symbol=request.COOKIES['name'])
    asset_balance_currency = client.get_asset_balance(asset=asset['quoteAsset'])
    asset_balance_coin = client.get_asset_balance(asset=asset['baseAsset'])
    return render(request, 'spot_trade.html', {'symbol': info['symbol'], 'price': divine_number(info['lastPrice'], 4),
                                               'change': round(float(info['priceChangePercent']), 2),
                                               'asset': asset['baseAsset'], 'form': form,
                                               'currency': asset['quoteAsset'],
                                               'asset_balance_currency': asset_balance_currency['free'],
                                               'asset_balance_coin': asset_balance_coin['free'], 'buy_form': buy_form, 'sell_form': sell_form})
