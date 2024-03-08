from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()
    rating_average = serializers.FloatField()
    rating_count = serializers.FloatField()

    class Meta:
        model = Review
        fields = ('__all__')
