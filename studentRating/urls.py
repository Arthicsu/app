from django.urls import path
from .views import radar_chart_view

urlpatterns = [
    path('chart/', radar_chart_view, name='chart'),
]
