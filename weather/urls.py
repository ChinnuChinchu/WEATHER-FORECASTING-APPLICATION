from django.urls import path
from .views import WeatherAPIView

urlpatterns = [
    path('weather/<str:cityname>/', WeatherAPIView.as_view(), name='weather_api'),
]