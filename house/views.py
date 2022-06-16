from django.http import HttpResponse
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from constants import NO_ACCESS_UPDATE_REVIEW, NO_ACCESS_UPDATE_HOUSE_IMAGE
from house.models import House, Amenities, HouseReview, SiteReview, HouseImages
from house.serializers import HouseSerializer, AmenitiesSerializer, HouseReviewSerializer, HouseReviewUpdateSerializer, \
    SiteReviewSerializer, SiteReviewUpdateSerializer


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


class AddHouse(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
               mixins.RetrieveModelMixin):
    """
    View to add House Details
    """
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return HttpResponse('invalid')

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class HouseView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """
    View to get, update, delete House Details
    """
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        request.data['user'] = request.user.id
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


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
