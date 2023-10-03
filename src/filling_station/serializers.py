from rest_framework import serializers
from .models import FillingStation, FavouriteStation


class PetrolProductSerializer(serializers.ModelSerializer):
    """Serializes petrol products"""

    class Meta:
        model = FillingStation
        fields = ['petrol_price', 'kerosene_price', 'diesel_price']


class StationAmenitiesSerializer(serializers.ModelSerializer):
    """Serializes station amenitieis"""

    class Meta:
        model = FillingStation
        fields = ['car_wash', 'pos', 'car_mechanic', 'mini_mart']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializes station amenities"""

    class Meta:
        model = FillingStation
        fields = ['name', 'operation_time', 'phone' ,'address']


class GetStationsByDistanceSerializer(serializers.ModelSerializer):
    """Serializer that returns details of all sations"""
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = FillingStation
        fields = ['license_number', 'petrol_price', 'kerosene_price', 'user', 'is_open', 'created_at', 'longitude', 'latitude',
                  'diesel_price', 'filling_station_slug', 'rating', 'name', 'address', 'phone', 'is_verified', 'distance_km']

    def get_distance_km(self, obj):
        # Access the distance attribute from the object and convert it to kilometers
        # return obj.distance.km if obj.distance else None
        if hasattr(obj, 'distance'):
            return obj.distance.km
        return None


class AddStationToFavoriteSerializer(serializers.ModelSerializer):
    """serializes a favouriteStation model for creation"""

    class Meta:
        model = FavouriteStation
        fields = ['user', 'station']
