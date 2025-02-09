from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.student_rating, name='student_rating'),
]