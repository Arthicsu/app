from django.urls import path
from .views import student_profile

app_name = 'studentProfile'

urlpatterns = [
    path('profile/<int:student_id>/', student_profile, name='student_profile'),
]