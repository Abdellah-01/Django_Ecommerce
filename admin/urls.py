from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'admin'

urlpatterns = [
    path('overview', views.overview, name='overview_admin_page'),
]
