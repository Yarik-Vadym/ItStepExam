from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('coins/', views.CoinsListView.as_view(), name='coins-list'),
    path('coins/<int:pk>/', views.CoinDetailView.as_view(), name='coin-detail'),
]
