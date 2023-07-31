from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings
from rest_framework.decorators import action, api_view, permission_classes
# import CreateFillingStation, CreateUserSerializer, UpdateUserSerializer, GetUserSerializer
from accounts.api import serializers as s
from rest_framework.response import Response
from rest_framework import status
from .models import User, GeneralUser
from filling_station.models import FillingStation


# Note --->  General User Role --> 1
# Note ---> Station Role --> 2

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
# @permission_classes([])
def get_users(request):
    """Returns all registered users"""

    all_users = GeneralUser.objects.all()
    serializer = s.GetUserSerializer(all_users, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
# @permission_classes([])
def get_user(request):
    """Returns all registered users"""


@api_view(["POST"])
# @permission_classes([])
def create_general_user(request):
    """Endpoint for creating a normal day to day customer"""

    serializer = s.CreateUserSerializer(data=request.data)

    if serializer.is_valid():
        role = 1
        serializer.save(role=role)

        return Response(
            {'message': "User created succesfully"},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PATCH"])
def update_general_user(request):
    """Endpoint for updating a normal day to nday user"""

    user_id = request.data.get("id")

    try:
        user = GeneralUser.objects.get(user=user_id)
    except GeneralUser.DoesNotExist:
        return Response(
            {'error': "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = s.UpdateUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'user': "User updated successfully"},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
def delete_general_user(request):
    """Endpoint Deleting an existing user"""

    user_id = request.data.get('user_id')

    try:
        user = User.objects.get(id=user_id)
    except:
        return Response(
            {'error': "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    user.delete()
    return Response({"message": "User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_station(request):
    """Creates a station account"""

    """Endpoint for creating a normal day to day customer"""

    serializer = s.CreateFillingStation(data=request.data)

    if serializer.is_valid():
        role = 2
        serializer.save(role=role)

        return Response(
            {'message': "Station created succesfully"},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
def delete_station(request):
    """Endpoint for deleting a station"""

    station_id = request.data.get("station_id")

    try:
        filling_station = User.objects.get(id=station_id)
        filling_station.delete()
        return Response(
            {"message": "Station deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    except:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
def update_station(request):
    """Endpoint to update an endpoint"""

    station_id = request.data.get('user')

    try:
        user = FillingStation.objects.get(user=station_id)
    except FillingStation.DoesNotExist:
        return Response(
            {"error": "Station does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = s.UpdateStation(user, data=request.data)
    if serializer.is_valid():
        print(f"Petrol price: {serializer.validated_data['petrol_price']}")
        print(f"Kerosene: {serializer.validated_data['kerosene_price']}")
        print(f"Diesel: {serializer.validated_data['diesel_price']}")
        serializer.save()

        return Response(
            {"message": "User successfully updated"},
            status=status.HTTP_200_OK
        )

    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_stations_by_slug(request, slug):
    """Endpoint to get all stations"""

    # slug = request.data.get('station_slug')
    try:
        station_profile = FillingStation.objects.get(filling_station_slug=slug)
    except FillingStation.DoesNotExist:
        return Response(
            {"error": "Station does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = s.GetStations(station_profile)
    return Response(
        {"station": serializer.data},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_stations(request):
    """Endpoint to get all stations"""

    all_stations = FillingStation.objects.all()

    serializer = s.GetStations(all_stations, many=True)
    return Response(
        {"stations":  serializer.data},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_admin_statistics(request):
    """Return all admin dashboard statistics"""

    all_stations = FillingStation.objects.all().count()
    verified_stations = FillingStation.objects.filter(is_verified=True).count()
    pending_stations = FillingStation.objects.filter(is_verified=False).count()

    data = {
        'all_stations': all_stations,
        'verified_stations': verified_stations,
        'pending_verification_stations': pending_stations
    }

    serializer = s.StatisticsSerializer(data=data)

    if serializer.is_valid():
        validated_data = serializer.validated_data

        return Response(
            {'statistics': validated_data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
