from rest_framework import serializers
from accounts.models import GeneralUser, User
from filling_station.models import FillingStation
from django.contrib.auth.hashers import make_password


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for creation of a user"""
    username = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'username']
        extra_kwargs = {
            # Make sure password is write-only
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        phone = validated_data.pop('phone_number')
        username = validated_data.pop('username')

        user = User.objects.create(**validated_data)
        GeneralUser.objects.create(
            phone=phone, user=user, username=username
        )

        return user
        # return super().create(validated_data)


class CreateFillingStation(serializers.ModelSerializer):
    """Serializer for creation of a staff profile"""
    latitude = serializers.CharField(max_length=20)
    longitude = serializers.CharField(max_length=20)
    license_number = serializers.CharField(max_length=20)
    name = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'license_number',
                  'name', 'longitude', 'latitude', 'phone_number']
        extra_kwargs = {
            # Make sure password is write-only
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print("Hello create block")
        name = validated_data.pop('name')
        longitude = validated_data.pop('longitude')
        latitude = validated_data.pop('latitude')
        license_number = validated_data.pop('license_number')
        phone_number = validated_data.pop('phone_number')
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        FillingStation.objects.create(
            user=user, name=name, license_number=license_number, longitude=longitude, latitude=latitude, phone=phone_number)

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer for updating a user"""

    class Meta:
        model = GeneralUser
        fields = ['phone', 'avatar', 'username']


class GetUserSerializer(serializers.ModelSerializer):
    """Serializer for getting all users"""

    class Meta:
        model = GeneralUser
        fields = ['username', 'created_at', 'phone', 'user']


class GetStations(serializers.ModelSerializer):
    """Serializer that returns details of all sations"""

    class Meta:
        model = FillingStation
        fields = ['license_number', 'petrol_price', 'kerosene_price', 'user', 'is_open', 'created_at', 'longitude', 'latitude',
                  'diesel_price', 'filling_station_slug', 'rating', 'name', 'address', 'phone', 'is_verified']


class UpdateStation(serializers.ModelSerializer):
    """Serializer that returns details of all sations"""

    class Meta:
        model = FillingStation
        fields = ['petrol_price', 'kerosene_price', 'diesel_price',
                  'name', 'station_img', 'address', 'phone', 'is_open', 'user']


class StatisticsSerializer(serializers.Serializer):
    """Serializer for all admin statistics"""

    all_stations = serializers.IntegerField()
    verified_stations = serializers.IntegerField()
    pending_verification_stations = serializers.IntegerField()
    all_users = serializers.IntegerField()


class GeneralUserProfileSerializer(serializers.ModelSerializer):
    """Serilalizes a general user object"""

    class Meta:
        model = GeneralUser
        fields = ['user', 'username', 'phone', 'avatar']
