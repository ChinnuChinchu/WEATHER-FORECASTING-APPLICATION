from django.shortcuts import render


# Create your views here.
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
import requests

from django.http import JsonResponse
from rest_framework import status
from rest_framework import authentication, permissions 
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


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
                necessary_items.extend(['Sunscreen', 'Water', 'Umbrella'])

            if temperature_celsius <= 21:
                necessary_items.extend(["Sweaters", "Boots", "Vacuum flask"])

            if 'overcast clouds' in weather_data['weather'][0]['description'].lower():
                necessary_items.extend(['Umbrella or Raincoat', 'Waterproof Travelbag', 'Quick Drying clothes'])

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
            api_key = 'bA5fH94W7CSKWSua1OU25VGwONXn7GA5'
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
            api_key = 'bA5fH94W7CSKWSua1OU25VGwONXn7GA5'
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
            api_key = 'bA5fH94W7CSKWSua1OU25VGwONXn7GA5'
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
            api_key = 'bA5fH94W7CSKWSua1OU25VGwONXn7GA5'
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
        
################################ 5dayweatherdata to save historical weather data #############################3
        
class AccuWeatherDayForecastHistorical(APIView):
    def get(self, request):
        try:
            # Your existing code to fetch forecast data
            api_key = 'bA5fH94W7CSKWSua1OU25VGwONXn7GA5'
            location_key = '2196366'
            url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                daily_forecasts = data.get('DailyForecasts', [])

                # Save forecast data into the database
                for forecast in daily_forecasts:
                    date_str = forecast.get('Date')
                    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')

                    # Check if a record with the same date already exists
                    if not WeatherForecast.objects.filter(date=date).exists():
                        temperature_min = forecast.get('Temperature').get('Minimum').get('Value')
                        temperature_max = forecast.get('Temperature').get('Maximum').get('Value')
                        
                        # Check if precipitation data is available
                        precipitation_data = forecast.get('Day', {}).get('PrecipitationProbability')
                        # Set default value if precipitation data is not available
                        precipitation = precipitation_data if precipitation_data is not None else 0

                        WeatherForecast.objects.create(date=date, temperature_min=temperature_min, temperature_max=temperature_max, precipitation=precipitation)

                # Serialize the saved data
                forecasts = WeatherForecast.objects.all()
                serializer = WeatherForecastSerializer(forecasts, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'Failed to fetch forecast data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
########################## notification of current weather data ################################

class WeatherNotificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

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
                necessary_items.extend(['Sunscreen', 'Water', 'Umbrella'])

            if temperature_celsius <= 21:
                necessary_items.extend(["Sweaters", "Boots", "Vacuum flask"])

            if 'overcast clouds' in weather_data['weather'][0]['description'].lower():
                necessary_items.extend(['Umbrella or Raincoat', 'Waterproof Travelbag', 'Quick Drying clothes'])

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

            # Send email notification to the current user
            user_email = request.user.email
            subject = 'Weather Notification'
            message = f"Hello {request.user.username},\n\nCurrent weather in {cityname}:\nTemperature: {temperature_celsius}°C\nHumidity: {weather_data['main']['humidity']}%\nDescription: {weather_data['weather'][0]['description']}\n\nNecessary Items: {', '.join(necessary_items)}"
            from_email = 'pchinchu003@gmail.com'  # Your sender email
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)

            return Response(serialized_data)
        else:
            if response.status_code == 404:
                return Response({'message': 'Weather data not found'}, status=404)
            else:
                return Response({'message': 'Failed to retrieve weather data'}, status=response.status_code)