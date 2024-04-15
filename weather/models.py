from django.db import models

# Create your models here.


class WeatherForecast(models.Model):
    date = models.DateField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    precipitation = models.FloatField()