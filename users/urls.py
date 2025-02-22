from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registration/', views.user_registration, name='registration'),
    path('', views.user_logout, name='logout'),
]