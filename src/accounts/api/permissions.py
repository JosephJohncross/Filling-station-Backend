from rest_framework import serializers
from accounts.models import StationUser, GeneralUser

class CreateUserSerializer(serializers.ModelSerializer):
    """Serializes object for creating a user"""
    
    class Meta:
        model = GeneralUser

class CreateStationSerializer(serializers.ModelSerializer):
    """Serializes object for creating a station user"""
    license_number = serializers.IntegerField()


    class Meta:
        model = StationUser
        fields = ['email', 'license_number']