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
    path('products/<str:product_slug>', views.view_product, name='view_products_admin_page'),
    path('collections', views.collections, name='collections_admin_page'),
    path('categories', views.categories, name='categories_admin_page'),

    # Orders
    path('orders', views.orders, name='orders_admin_page'),
    path('abandoned_checkouts', views.abandoned_checkouts, name='abandoned_checkouts_admin_page')
]
