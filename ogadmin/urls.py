from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'ogadmin'

urlpatterns = [
    # Authentication
    path('login', views.login, name='login_admin_page'),
    path('forget_password', views.forget_password, name='forget_password_admin_page'),
    path('logout', views.logout, name='logout_admin_page'),

    # Products
    path('', views.dashboard, name='dashboard_admin_page1'),
    path('dashboard', views.dashboard, name='dashboard_admin_page'),
    path('products', views.products, name='products_admin_page'),
]
