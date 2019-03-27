# omdbsearch/urls.py

from django.conf.urls import url
from django.urls import path, include

from omdbsearch import views

urlpatterns = [
  path('', views.index, name='index'),
  path('main/', views.search, name='search'),
  path('home/', views.home, name='home'),
]