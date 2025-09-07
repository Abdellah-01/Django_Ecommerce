from django.urls import path
from . import views
app_name = "accounts"

urlpatterns = [
    # User Authentication
    path('register', views.register, name='register_page'),
    path('login', views.login, name='login_page'),
    path('logout', views.logout, name='logout_page'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate_page'),
    path('lost-password', views.lost_password, name='lost_password_page'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate_page'),
    path('reset-password', views.reset_password, name='reset_password_page'),

    # USer Acoounts
    path('dashboard', views.dashboard, name='dashboard_page'),
    path('my_orders', views.my_orders, name='my_orders_page'),
]
