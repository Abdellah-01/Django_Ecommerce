from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path('track-order', views.track_order, name ="track_order_page"),
    path('return-exchange', views.return_exchange, name ="return_exchange_page")
]
