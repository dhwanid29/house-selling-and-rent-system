from django.http import HttpResponse
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from house.models import House, Amenities
from house.serializers import HouseSerializer, AmenitiesSerializer


# HouseReviewSerializer


class AddAmenities(generics.CreateAPIView):
    serializer_class = AmenitiesSerializer
    permission_classes = [IsAdminUser]


class AmenitiesView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin):
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


# class HouseReviewView(generics.GenericAPIView, mixins.CreateModelMixin):
#     serializer_class = HouseReviewSerializer
#     permission_classes = [IsAuthenticated]


class AddHouse(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
               mixins.RetrieveModelMixin):
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
