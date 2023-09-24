from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from accounts.models import GeneralUser
from . import serializers
from .models import Review
from filling_station.models import FillingStation


@api_view(['POST'])
def create_a_review(request):
    """Creates a station review by a user"""

    serializer = serializers.CreateReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {"message": "Review made successfully"},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
def delete_a_review(request, id):
    """Deletes a user review"""

    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(
            {"error": "review not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    review.delete()
    return Response(
        {"message": "Review deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(["GET"])
def get_station_review(request, id):
    """Returns a station review"""

    try:
        station = FillingStation.objects.get(id=id)
    except FillingStation.DoesNotExist:
        return Response(
            {"error": "Station does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    reviews = Review.objects.filter(station=station)

    all_review = []

    for review in reviews:
        review_data = {
            "user": review.user_id,
            "station": review.station_id,
            "review": review.review,
            "date": review.date_of_review,
            "user_profile_picture": review.user.avatar,
            "name": review.user.name
        }

        all_review.append(review_data)

    return JsonResponse({"reviews": all_review}, safe=False)
