from django.urls import path
from . import views

urlpatterns = [
    path('', views.collections_list, name = 'collections_page'),
    path('all', views.all_products_collections, name = 'collections_page'),
    path('<str:collection_slug>/', views.all_products_collections, name='products_by_collection_page')
]
