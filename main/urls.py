from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.student_rating, name='student_rating'),
    # path('student/<int:student_id>/', views.student_profile, name='student_profile'),
]