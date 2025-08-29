from django.urls import path
from . import views

app_name = 'carts_urls'

urlpatterns = [
    path('', views.view_cart, name = 'view_cart_page'),
    path('add_cart/<int:product_id>/', views.add_cart, name = 'add_cart_page'),
    path('remove_cart/<int:cart_item_id>/', views.remove_cart, name='remove_cart_page'),
    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item_page'),
    path('checkout', views.checkout, name='checkout_page')
]
