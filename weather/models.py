from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class WeatherForecast(models.Model):
    date = models.DateField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    precipitation = models.FloatField()
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"