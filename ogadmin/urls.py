from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'ogadmin'

urlpatterns = [
    path('overview', views.overview, name='overview_admin_page'),
    path('login', views.login, name='login_admin_page'),
    path('forget_password', views.forget_password, name='forget_password_admin_page'),
    path('logout', views.logout, name='logout_admin_page'),
]
