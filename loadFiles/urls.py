from django.urls import path
from .views import upload_achievement

app_name = 'loadFiles'

urlpatterns = [
    path('upload/', upload_achievement, name='upload'),
]