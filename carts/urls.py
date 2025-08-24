from django.urls import path
from . import views

app_name = 'carts_urls'

urlpatterns = [
    path('', views.view_cart, name = 'view_cart_page')
]
