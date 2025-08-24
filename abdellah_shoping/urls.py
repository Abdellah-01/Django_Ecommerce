from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'abdellah_shoping'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('search', views.search, name='search_page')
]
