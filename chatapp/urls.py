# chatapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # A raiz do aplicativo carrega a view index
    path('search/', views.search, name='search'),
]
