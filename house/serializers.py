from rest_framework import serializers
from house.models import House, Amenities, HouseReview, SiteReview, HouseImages


class AmenitiesSerializer(serializers.ModelSerializer):
    """
    Serializer for amenities
    """
    class Meta:
        model = Amenities
        fields = '__all__'


class SiteReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Site Review
    """
    class Meta:
        model = SiteReview
        fields = '__all__'


class SiteReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Site Review Update
    """
    class Meta:
        model = SiteReview
        fields = ['review']


class HouseSerializer(serializers.ModelSerializer):
    """
    Serializer for House
    """
    class Meta:
        model = House
        fields = '__all__'


class HouseImageSerializer(serializers.ModelSerializer):
    """
    Serializer for House Images
    """
    class Meta:
        model = HouseImages
        fields = '__all__'


class HouseReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for House Review Update
    """
    class Meta:
        model = HouseReview
        fields = ['review']


class HouseReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for House Review
    """
    class Meta:
        model = HouseReview
        fields = '__all__'