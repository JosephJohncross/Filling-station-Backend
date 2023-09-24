from rest_framework import serializers
from .models import Review


class CreateReviewSerializer(serializers.ModelSerializer):
    """Serializes a review model object"""

    class Meta:
        model = Review
        fields = ['user', 'review', 'station']
