from django.urls import path
from . import views
app_name = "accounts"

urlpatterns = [
    # User Authentication
    path('register', views.register, name='register_page'),
    path('login', views.login, name='login_page'),
    path('logout', views.logout, name='logout_page'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate_page'),

    # USer Acoounts
    path('dashboard', views.dashboard, name='dashboard_page')
]
