from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
import requests

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