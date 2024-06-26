from django.contrib.auth.models import User

from .models import *
from  rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    temperature = serializers.FloatField()
    humidity = serializers.IntegerField()
    description = serializers.CharField()
    


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = '__all__'