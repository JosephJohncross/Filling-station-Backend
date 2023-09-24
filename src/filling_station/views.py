from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import FillingStation
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


@api_view(['PATCH'])
def set_is_open_status(request):
    """Sets a filling station operation time to open or close"""

    open_status = request.data.get('is_open')
    print(open_status)
    user = request.data.get('user')

    try:
        station = FillingStation.objects.get(user_id=user)

        station.is_open = bool(int(open_status))
        station.save()
        print(station.is_open)

        return Response(
            "",
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            e,
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
def edit_fuel_products(request):
    """Update petro product price"""

    user_id = request.data.get('user_id')
    try:
        filling_station = FillingStation.objects.get(user_id=user_id)
    except FillingStation.DoesNotExist:
        return Response(
            {"Message": "Filling station does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = serializers.PetrolProductSerializer(
        filling_station, request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(
            {"message": "Products updated successfully"},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PATCH'])
def edit_station_amenities(request):
    """Update station amenities"""

    user_id = request.data.get('user_id')
    try:
        filling_station = FillingStation.objects.get(user_id=user_id)
    except FillingStation.DoesNotExist:
        return Response(
            {"Message": "Filling station does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = serializers.StationAmenitiesSerializer(
        filling_station, request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(
            {"message": "Products updated successfully"},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PATCH'])
def edit_station_profile(request):
    """Update station amenities"""

    user_id = request.data.get('user_id')
    try:
        filling_station = FillingStation.objects.get(user_id=user_id)
    except FillingStation.DoesNotExist:
        return Response(
            {"Message": "Filling station does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = serializers.ProfileSerializer(filling_station, request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(
            {"message": "Profile updated successfully"},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_all_stations_in_my_location(request):
    """Get all the stations in a particuar location"""

    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longtitude')
    # latitude = request.data.get('latitude')
    # longitude = request.data.get('longitude')

    user_location = Point(float(longitude), float(latitude), srid=4326)

    close_stations = FillingStation.objects.annotate(
        distance=Distance('location', user_location)
    ).filter(distance__lte=3000).order_by('distance')

    serializer = serializers.GetStationsByDistanceSerializer(
        close_stations, many=True, context={'user_location': user_location})

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
