from warnings import filters

import django_filters
from django.http import HttpResponse
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from constants import NO_ACCESS_UPDATE_REVIEW, NO_ACCESS_UPDATE_HOUSE_IMAGE
from house.models import House, Amenities, HouseReview, SiteReview, HouseImages, Likes
from house.serializers import HouseSerializer, AmenitiesSerializer, HouseReviewSerializer, HouseReviewUpdateSerializer, \
    SiteReviewSerializer, SiteReviewUpdateSerializer, HouseImageSerializer, LikesSerializer


class AddAmenities(generics.CreateAPIView):
    """
    View to Add Amenities
    """
    serializer_class = AmenitiesSerializer
    permission_classes = [IsAdminUser]


class AmenitiesView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin):
    """
    View to get, update and delete amenities
    """
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

    def get(self, request, id=None):
        return self.retrieve(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


# class PriceFilter(django_filters.FilterSet):
#     price = django_filters.RangeFilter()
#
#     class Meta:
#         model = House
#         fields = ['price']


class HouseViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete House Details
    """
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = PriceFilter
    filterset_fields = ['amenities', 'no_of_bedrooms']
    search_fields = '__all__'
    ordering_fields = '__all__'

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        instance = self.get_object()
        if instance.user.id == request.user.id:
            serializer = HouseSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_REVIEW}, status=status.HTTP_400_BAD_REQUEST)


class SiteReviewViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete Site Review
    """
    serializer_class = SiteReviewSerializer
    queryset = SiteReview.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            serializer = SiteReviewUpdateSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_REVIEW}, status=status.HTTP_400_BAD_REQUEST)


class HouseReviewViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete House Review
    """
    serializer_class = HouseReviewSerializer
    queryset = HouseReview.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['review']
    search_fields = ['review']
    ordering_fields = ['review']

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            request.data['house'] = instance.house.id
            serializer = HouseReviewUpdateSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_REVIEW}, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object(house)
    #     print(instance, '----------------------------------------------------------------------')
    #     print('hie', instance)
    #     house_review_queryset = HouseReview.objects.filter(house=instance)
    #     print(house_review_queryset)
    #     house_review_serializer = HouseReviewSerializer(house_review_queryset, many=True)
    #     return Response(house_review_serializer.data, status=status.HTTP_200_OK)


class HouseImageViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete House Image
    """
    serializer_class = HouseImageSerializer
    queryset = HouseImages.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            request.data['house'] = instance.house.id
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_HOUSE_IMAGE}, status=status.HTTP_400_BAD_REQUEST)


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        house_obj = House.objects.get(pk=request.data.get('house'))
        print(house_obj.id)
        like, created = Likes.objects.get_or_create(house=house_obj)
        print(like, 'njsd')
        print(created, 'jzdshj')
        like.user.add(request.user)

        all_likes = Likes.objects.get(house=house_obj)
        serializer = LikesSerializer(all_likes, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
