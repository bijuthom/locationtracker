from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserLocation(models.Model):
    id=models.BigAutoField(primary_key='true')
    location=models.CharField(max_length=200)
    latitude=models.FloatField()
    longitude=models.FloatField()
    loctime=models.DateTimeField(auto_now=False, auto_now_add=False)
    updated=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)