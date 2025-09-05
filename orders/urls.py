from django.urls import path
from . import views

app_name = "orders_urls"

urlpatterns = [
    path('place_order', views.place_order, name ="place_order_page"),
    path('review_order', views.make_payment, name="review_order_page")
]
