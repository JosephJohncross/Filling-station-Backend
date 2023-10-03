from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from .models import FillingStation, FavouriteStation
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import JsonResponse
from accounts.models import User
from cloudinary.uploader import upload
from rest_framework.parsers import FileUploadParser
from django.db.models import Q
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import ACos, Cos, Radians, Sin


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


@api_view(['PATCH'])
def rate_station(request):
    """Rates a station"""

    station_id = request.data.get('station_id')
    rating = request.data.get('rating')

    try:
        station = FillingStation.objects.get(id=station_id)
    except FillingStation.DoesNotExist:
        return Response(
            {"error": "Station not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    station.no_of_user_rating += 1
    station.total_rating += int(rating)
    station.rating = str(round(station.total_rating /
                         station.no_of_user_rating, 1))
    station.save()

    return Response(
        {"rating": station.rating},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def add_station_to_favorite(request):
    """Adds a single station to a user favorite"""

    user_id = request.data.get('user')
    station_id = request.data.get('station')

    try:
        favorite_station = FavouriteStation.objects.get(
            station=station_id, user=user_id)
        return Response(
            {"message": "Station already in favorite"},
            status=status.HTTP_200_OK
        )
    except:
        serializer = serializers.AddStationToFavoriteSerializer(
            data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Station added to favourites"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
def get_favourite_station(request, user_id):
    """Returns all favourite stations added by the user"""

    try:
        favourite_station = FavouriteStation.objects.filter(
            user=user_id).values_list('station', flat=True)
        print(favourite_station)
    except FavouriteStation.DoesNotExist:
        return Response(
            {"error": "User does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    my_favourite = []
    for station in favourite_station:
        filling_station = FillingStation.objects.get(id=station)
        print(filling_station)
        station_profile = {
            'address': filling_station.address,
            'petrol_price': filling_station.petrol_price,
            'kerosene_price': filling_station.kerosene_price,
            'diesel_price': filling_station.diesel_price,
            'rating': filling_station.rating,
            'is_open': filling_station.is_open,
            'operation_time': filling_station.operation_time,
            'name': filling_station.name,
            'user': filling_station.user_id,
            'station_id':  filling_station.id
        }
        my_favourite.append(station_profile)

    return JsonResponse({"favourite": my_favourite})


@api_view(['DELETE'])
def remove_favourite(request, station, user):
    """Deletes a favourite from a user favourite list"""

    try:
        favourite = FavouriteStation.objects.get(station=station, user=user)
    except:
        return Response(
            {"error": "Station not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    favourite.delete()

    return Response(
        {"message": "Station removed from favourtites"},
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['PATCH'])
def verify_station(request, id):
    """Set station verification statues"""

    try:
        user = FillingStation.objects.get(user=id)
        print(user)
    except User.DoesNotExist:
        return Response(
            {"error": "User does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    user.is_verified = True
    user.save()

    return Response(
        {"message": "Station verified"},
        status=status.HTTP_200_OK
    )


@api_view(['PATCH'])
@parser_classes([FileUploadParser])
def update_station_img(request):
    """Updates to station image"""

    station_id = request.data.get('station_id')
    if request.method == 'PATCH' and 'image' in request.data:
        image = request.data['image']

    try:
        station = FillingStation.objects.get(id=station_id)

        response = upload(image)
        cloudinary_url = response['secure_url']
        station.station_img = cloudinary_url
        return Response({
            "message": "Image upload successful"
        })
    except FillingStation.DoesNotExist:
        return Response(
            {"error": "station does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def user_station_search(request):
    """Search functionality for login users"""

    search_term = request.query_params.get('search_term', '')
    latitude = float(request.query_params.get('latitude', 0))
    longitude = float(request.query_params.get('longitude', 0))

    search_result = FillingStation.objects.filter(
        Q(address__icontains=search_term) | Q(name__icontains=search_term))

    # # Calculate distance using Haversine formula
    # distance_expression = ExpressionWrapper(
    #     6371.0 * ACos(
    #         Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) *
    #         Cos(Radians(F('longitude')) - Radians(longitude)) +
    #         Sin(Radians(latitude)) * Sin(Radians(F('latitude')))
    #     ),
    #     output_field=FloatField()
    # )

    # queryset = search_result.extra(select={'distance': distance_expression})
    # sett = search_result.extra(select={'distance', ''})
    # print(str(sett.query))

    serializer = serializers.GetStationsByDistanceSerializer(
        search_result, many=True)
    # if serializer.is_valid():
    return Response(
        {"search_result":  serializer.data},
        status=status.HTTP_200_OK
    )
    # else:
    #     return Response(
    #         {"errror": serializer.errors},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
