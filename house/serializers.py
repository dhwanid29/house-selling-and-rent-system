from rest_framework import serializers

from accounts.models import User
from house.models import House, Amenities, HouseReview, SiteReview, HouseImages, Likes, Favourites


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


class HouseImageSerializer(serializers.ModelSerializer):
    """
    Serializer for Site Review Update
    """

    class Meta:
        model = HouseImages
        fields = ['house', 'user', 'house_image']


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


class HouseImageForHouseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for House Images to display in house detail
    """

    class Meta:
        model = HouseImages
        fields = ['house_image']


class HouseReviewForHouseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for House review to display in house detail
    """

    class Meta:
        model = HouseReview
        fields = ['review']


class HouseSerializer(serializers.ModelSerializer):
    """
    Serializer for House
    """
    house_image_set = HouseImageForHouseDetailSerializer(many=True, read_only=True)
    house_review_set = HouseReviewForHouseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = '__all__'


class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = ['user', 'house']


class FavouritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourites
        fields = ['user', 'house']
