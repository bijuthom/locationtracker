'''
Created on Apr 10, 2018

@author: biju
'''
from rest_framework import serializers
from trackerapp.models import UserLocation
class LocationSerializer(serializers.ModelSerializer):
    class Meta:  
        model = UserLocation
        fields = ('id', 'location','latitude','longitude','loctime','user') 
        many=True       
    