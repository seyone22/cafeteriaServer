from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()
    rating = serializers.FloatField()
    site = serializers.CharField()

    class Meta:
        model = Review
        fields = ('__all__')
