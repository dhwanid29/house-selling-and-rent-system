from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from house.models import House, Amenities, HouseReview, SiteReview, HouseImages, Likes, Favourites, FavouritesUser, \
    Preference


class AmenitiesSerializer(serializers.ModelSerializer):
    """
    Serializer for amenities
    """

    class Meta:
        model = Amenities
        fields = ['name']


class SiteReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Site Review
    """

    class Meta:
        model = SiteReview
        fields = ['review']


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
        fields = ['house', 'house_image']


class HouseImageUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Site Review Update
    """

    class Meta:
        model = HouseImages
        fields = ['house', 'house_image']


class HouseImageSerializer(serializers.ModelSerializer):
    """
    Serializer for House Images
    """

    class Meta:
        model = HouseImages
        fields = ['user', 'house', 'house_image']


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
        fields = ['house', 'review']


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
        fields = ['review', 'user']


class LikesSerializerForHouseDetail(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = ['user']


class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = ['user', 'house']


class HouseSerializer(serializers.ModelSerializer):
    """
    Serializer for House
    """
    house_image_set = HouseImageForHouseDetailSerializer(many=True, read_only=True)
    house_review_set = HouseReviewForHouseDetailSerializer(many=True, read_only=True)
    house_likes_set = LikesSerializerForHouseDetail(many=True, read_only=True)

    class Meta:
        model = House
        fields = ['house_image_set', 'house_review_set', 'house_likes_set', 'amenities', 'residence_name', 'address', 'price', 'no_of_bedrooms', 'no_of_lift', 'no_of_floors',
                  'no_of_building', 'state', 'city', 'sqft', 'selling_choice', 'possession', 'project_status']


class HouseUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for House Update
    """
    house_image_set = HouseImageForHouseDetailSerializer(many=True, read_only=True)
    house_review_set = HouseReviewForHouseDetailSerializer(many=True, read_only=True)
    house_likes_set = LikesSerializerForHouseDetail(many=True, read_only=True)

    class Meta:
        model = House
        fields = ['house_image_set', 'house_review_set', 'house_likes_set', 'amenities', 'residence_name', 'address', 'price', 'no_of_bedrooms', 'no_of_lift', 'no_of_floors',
                  'no_of_building', 'state', 'city', 'sqft', 'selling_choice', 'possession', 'project_status',
                  'is_available']


class FavouritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourites
        fields = ['user', 'house']


class MyFavouritesSerializer(serializers.ModelSerializer):
    house_set = HouseSerializer(many=True, read_only=True)
    house = serializers.SerializerMethodField()
    residence_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = FavouritesUser
        fields = ['house', 'house_set', 'residence_name', 'address']

    def get_residence_name(self, obj):
        return obj.favourites.house.residence_name

    def get_address(self, obj):
        return obj.favourites.house.address

    def get_house(self, obj):
        return obj.favourites.house.id


class PreferencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = ['user', 'residence_name', 'no_of_bedrooms', 'state', 'city', 'selling_choice']