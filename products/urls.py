from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="products_page"),
    path("<str:product_slug>", views.product_details, name="product_details_page"),
]
