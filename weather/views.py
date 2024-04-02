from django.shortcuts import render


# Create your views here.
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
import requests

from django.http import JsonResponse
from rest_framework import status

class WeatherAPIView(APIView):
    def get(self, request, cityname):
        api_key = '8034387bb4a3826ba62baa311ea48856'

        url = f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            temperature_kelvin = weather_data['main']['temp']
            temperature_celsius = round(temperature_kelvin - 273.15)
            
            # Extracting necessary items based on weather conditions
            necessary_items = []

            if temperature_celsius > 22:
                necessary_items.append('Sunscreen')
                necessary_items.append('Water')
                necessary_items.append('Umbrella')

            if temperature_celsius <= 21:
                necessary_items.append("Sweaters")
                necessary_items.append("Boots")
                necessary_items.append("Vacuum flask")

            if 'overcast clouds' in weather_data['weather'][0]['description'].lower():
                necessary_items.append('Umbrella or Raincoat')
                necessary_items.append('Waterproof Travelbag')
                necessary_items.append('Quick Drying clothes')

            # Other conditions to add necessary items based on weather

            # Serialize weather data and necessary items
            serialized_data = {
                'weather': {
                    'city': cityname,
                    'temperature': temperature_celsius,
                    'humidity': weather_data['main']['humidity'],
                    'description': weather_data['weather'][0]['description']
                },
                'necessary_items': necessary_items
            }

            return Response(serialized_data)
        else:
            if response.status_code == 404:
                return Response({'message': 'Weather data not found'}, status=404)
            else:
                return Response({'message': 'Failed to retrieve weather data'}, status=response.status_code)
                
#1 Day of Daily Forecasts


class AccuWeatherOneDayForecast(APIView):
    def get(self, request):
        try:
            # Replace 'YOUR_API_KEY' with your actual AccuWeather API key
            api_key = '11Q2ffInM19875O2HQkqC9hkIdsYgTws'
            location_key = '2196366'  # Replace with your location key

            # Construct the URL
            url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}'

            # Make the request
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Return the forecast data as JSON response
                return Response(data)
            else:
                # If the request was not successful, return an error message
                return Response({'error': 'Failed to fetch daily forecast data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # If any exception occurs during the request, return an error message
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AccuWeather5DayForecast(APIView):
    def get(self, request):
        try:
            # Replace 'YOUR_API_KEY' with your actual AccuWeather API key
            api_key = '11Q2ffInM19875O2HQkqC9hkIdsYgTws'
            location_key = '2196366'  # Replace with your location key

            # Construct the URL
            url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={api_key}'

            # Make the request
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Split forecast data by date
                daily_forecasts = data.get('DailyForecasts', [])

                # Create a dictionary to hold forecast data for each date
                forecast_by_date = {}
                for forecast in daily_forecasts:
                    date = forecast.get('Date')
                    forecast_by_date[date] = forecast

                # Return the forecast data by date as JSON response
                return Response(forecast_by_date)
            else:
                # If the request was not successful, return an error message
                return Response({'error': 'Failed to fetch forecast data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # If any exception occurs during the request, return an error message
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

# 12 Hours of Hourly Forecasts


class AccuWeatherHourlyForecast(APIView):
    def get(self, request):
        try:
            # Replace 'YOUR_API_KEY' with your actual AccuWeather API key
            api_key = '11Q2ffInM19875O2HQkqC9hkIdsYgTws'
            location_key = '2196366'  # Replace with your location key

            # Construct the URL
            url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}?apikey={api_key}'

            # Make the request
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Return the forecast data as JSON response
                return Response(data)
            else:
                # If the request was not successful, return an error message
                return Response({'error': 'Failed to fetch hourly forecast data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # If any exception occurs during the request, return an error message
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
  
  
      
# 1 Hour of Hourly Forecasts  
      
class AccuWeatherOneHourlyForecast(APIView):
    def get(self, request):
        try:
            # Replace 'YOUR_API_KEY' with your actual AccuWeather API key
            api_key = '11Q2ffInM19875O2HQkqC9hkIdsYgTws'
            location_key = '2196366'  # Replace with your location key

            # Construct the URL
            url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}?apikey={api_key}'

            # Make the request
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Return the forecast data as JSON response
                return Response(data)
            else:
                # If the request was not successful, return an error message
                return Response({'error': 'Failed to fetch hourly forecast data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # If any exception occurs during the request, return an error message
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
