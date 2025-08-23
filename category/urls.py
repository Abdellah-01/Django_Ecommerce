from django.urls import path
from . import views

app_name = 'category_urls'

urlpatterns = [
    path('', views.category_list, name = 'category_page'),
    path('all', views.category_products, name = 'category_products_page'),
    path('<str:category_slug>', views.category_products, name = 'products_by_category_page'),
]
