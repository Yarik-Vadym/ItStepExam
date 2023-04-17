from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='blog'),
    path('<int:pk>/', blog, name='blog'),
    path('<int:pk>/edit/', edit_blog, name='edit_blog'),
    path('create_blog/', create_blog, name='create_blog'),
]