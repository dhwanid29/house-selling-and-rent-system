from rest_framework import serializers
from house.models import House, Amenities, HouseReview


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

# class HouseReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HouseReview
#         fields = '__all__'
