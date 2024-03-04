from django.urls import path
from .views import *

urlpatterns = [
    path('weather/<str:cityname>/', WeatherAPIView.as_view(), name='weather_api'),
    path('accuweather-one-day-forecast/', AccuWeatherOneDayForecast.as_view(), name='accuweather_one_day_forecast'),
    path('accuweather-5day-forecast/', AccuWeather5DayForecast.as_view(), name='accuweather_5day_forecast'),
    
    path('accuweather-hourly-forecast/', AccuWeatherHourlyForecast.as_view(), name='accuweather_hourly_forecast'),
    path('accuweather-one-hourly-forecast/', AccuWeatherOneHourlyForecast.as_view(), name='accuweather_one_hourly_forecast'),
    
]