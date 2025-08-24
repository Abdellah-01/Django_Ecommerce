from django.urls import path
from . import views

app_name = 'carts_urls'

urlpatterns = [
    path('', views.view_cart, name = 'view_cart_page'),
    path('add_cart/<int:product_id>/', views.add_cart, name = 'add_cart_page')
]
