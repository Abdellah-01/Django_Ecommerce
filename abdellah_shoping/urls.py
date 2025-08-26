from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'abdellah_shoping'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('search', views.search, name='search_page'),
    path('search_here', views.search_here, name='search_here_page'),
    path('faq', views.faq, name='faq_page'),
    path('contact', views.contact, name='contact_page')
]
