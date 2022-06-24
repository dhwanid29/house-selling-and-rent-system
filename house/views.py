from warnings import filters

import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from accounts.models import User
from accounts.utils import EmailSend
from constants import NO_ACCESS_UPDATE_REVIEW, NO_ACCESS_UPDATE_HOUSE_IMAGE, DISLIKE_ERROR, LIKE_ERROR, FAVOURITE_ERROR, \
    REMOVE_FAVOURITES_ERROR, EMAIL_BODY_FAVOURITES, EMAIL_SUBJECT_FAVOURITES, NOT_REGISTERED, HOUSE_DOES_NOT_EXIST, \
    HOUSE_CREATED, HOUSE_UPDATED, REVIEW_CREATED, REVIEW_UPDATED, LIKED, UNLIKED, ADDED_TO_FAVOURITES, \
    REMOVED_FAVOURITES
from house.models import House, Amenities, HouseReview, SiteReview, HouseImages, Likes, LikesUser, Favourites, \
    FavouritesUser
from house.serializers import HouseSerializer, AmenitiesSerializer, HouseReviewSerializer, HouseReviewUpdateSerializer, \
    SiteReviewSerializer, SiteReviewUpdateSerializer, HouseImageSerializer, LikesSerializer, FavouritesSerializer, \
    MyFavouritesSerializer, HouseUpdateSerializer, HouseImageUpdateSerializer


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


class HouseViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete House Details
    """
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': HOUSE_CREATED}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        instance = self.get_object()
        if instance.user.id == request.user.id:
            serializer = HouseUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({'data': serializer.data, 'msg': HOUSE_UPDATED}, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_REVIEW}, status=status.HTTP_400_BAD_REQUEST)


class SiteReviewViewSet(viewsets.ModelViewSet):
    """
    View to add, get, update, delete Site Review by id
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
        return Response({'data': serializer.data, 'msg': REVIEW_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            serializer = SiteReviewUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({'data': serializer.data, 'msg': REVIEW_UPDATED}, status=status.HTTP_200_OK)
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
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house)
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': REVIEW_CREATED}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            request.data['house'] = instance.house.id
            serializer = HouseReviewUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({'data': serializer.data, 'msg': REVIEW_UPDATED}, status=status.HTTP_200_OK)
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
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house)
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': HOUSE_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            request.data['house'] = instance.house.id
            serializer = HouseImageUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'data': serializer.data, 'msg': HOUSE_UPDATED}, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_HOUSE_IMAGE}, status=status.HTTP_400_BAD_REQUEST)


class LikesViewSet(viewsets.ModelViewSet):
    """
    View to Like and Dislike House
    """
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    lookup_field = 'house'
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house)
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        house_obj = House.objects.get(pk=request.data.get('house'))
        liked_user = Likes.objects.filter(house=house_obj.id).values('user')
        liked_user_lists = []
        for user in liked_user:
            liked_user_lists.append(str(user['user']))
        if str(request.user.id) not in liked_user_lists:
            like, created = Likes.objects.get_or_create(house=house_obj)
            like.user.add(request.user)
            all_likes = Likes.objects.get(house=house_obj)
            serializer = LikesSerializer(all_likes, many=False)

            return Response({'data': serializer.data, 'msg': LIKED}, status=status.HTTP_201_CREATED)
        return Response({'msg': LIKE_ERROR}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        request.data['house'] = instance.house.id
        house_obj = House.objects.get(pk=request.data.get('house'))
        liked_user = Likes.objects.filter(house=instance.house.id).values('user')
        for user in liked_user:
            if user['user'] == request.user.id:
                instance.user.remove(request.user)
                all_likes = Likes.objects.get(house=house_obj)
                serializer = self.get_serializer(all_likes, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response({'data': serializer.data, 'msg': UNLIKED}, status=status.HTTP_200_OK)
        return Response({'msg': DISLIKE_ERROR}, status=status.HTTP_204_NO_CONTENT)


class FavouritesViewSet(viewsets.ModelViewSet):
    """
    View to Shortlist House and remove House from Shortlisted list
    """
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer
    lookup_field = 'house'
    permission_classes = [IsAuthenticated]

    def create(self, request, attrs=None, *args, **kwargs):
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house)
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        house_obj = House.objects.get(pk=request.data.get('house'))
        favourited_user = Favourites.objects.filter(house=house_obj.id).values('user')
        favourited_user_lists = []
        for user in favourited_user:
            favourited_user_lists.append(str(user['user']))
        if str(request.user.id) not in favourited_user_lists:
            favourite, created = Favourites.objects.get_or_create(house=house_obj)
            favourite.user.add(request.user)
            email = house_obj.user.email
            user = User.objects.filter(email=email).first()
            try:
                # Send Mail
                data = {'subject': EMAIL_SUBJECT_FAVOURITES,
                        'body': EMAIL_BODY_FAVOURITES + "\nUser Details:" + "\nName - " + request.user.first_name +
                                request.user.last_name + "\nEmail - " + request.user.email + "\nPhone Number - " +
                                str(request.user.phone_number), 'to_email': user.email}
                EmailSend.send_email(data)
            except:
                return Response({'msg': NOT_REGISTERED}, status=status.HTTP_404_NOT_FOUND)
            all_favourites = Favourites.objects.get(house=house_obj)
            serializer = FavouritesSerializer(all_favourites, many=False)

            return Response({'data': serializer.data, 'msg': ADDED_TO_FAVOURITES}, status=status.HTTP_201_CREATED)
        return Response({'msg': FAVOURITE_ERROR}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data['house'] = instance.house.id
        house_obj = House.objects.get(pk=request.data.get('house'))
        favourited_user = Favourites.objects.filter(house=instance.house.id).values('user')
        for user in favourited_user:
            if user['user'] == request.user.id:
                instance.user.remove(request.user)
                all_favourites = Favourites.objects.get(house=house_obj)
                serializer = self.get_serializer(all_favourites, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response({'data': serializer.data, 'msg': REMOVED_FAVOURITES}, status=status.HTTP_200_OK)
        return Response({'msg': REMOVE_FAVOURITES_ERROR}, status=status.HTTP_204_NO_CONTENT)


class BuyerHouseRetrieveView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    View to display available house details to buyer
    """
    queryset = House.objects.filter(is_available=True).filter(selling_choice="Sell")
    serializer_class = HouseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class BuyerHouseListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to display available house list to buyer
    """
    queryset = House.objects.filter(is_available=True).filter(selling_choice="Sell")
    serializer_class = HouseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        sort_by_price_asc = request.GET.get('sort_by_price_asc')
        sort_by_price_desc = request.GET.get('sort_by_price_desc')
        filter_city = request.GET.get('filter_city')
        filter_state = request.GET.get('filter_state')
        filter_amenities = request.GET.get('filter_amenities')
        filter_no_of_bedrooms = request.GET.get('filter_no_of_bedrooms')
        filter_possession = request.GET.get('filter_possession')
        filter_project_status = request.GET.get('filter_project_status')
        date_before = request.GET.get('date_before')
        date_after = request.GET.get('date_after')
        queryset = House.objects.filter(is_available=True).filter(selling_choice="Sell")

        if filter_city:
            queryset = queryset.filter(city=filter_city).order_by('-created_date')
        if filter_state:
            queryset = queryset.filter(state=filter_state).order_by('-created_date')
        if filter_amenities:
            queryset = queryset.filter(amenities=filter_amenities).order_by('-created_date')
        if filter_no_of_bedrooms:
            queryset = queryset.filter(no_of_bedrooms=filter_no_of_bedrooms).order_by('-created_date')
        if filter_possession:
            queryset = queryset.filter(possession=filter_possession).order_by('-created_date')
        if filter_project_status:
            queryset = queryset.filter(project_status=filter_project_status).order_by('-created_date')
        if search:
            queryset = queryset.filter(Q(city__contains=search) | Q(state__contains=search)).order_by('-created_date')
        if price_min and price_max:
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
        elif price_max:
            queryset = queryset.filter(price__lte=price_max)
        elif price_min:
            queryset = queryset.filter(price__gte=price_min)
        if date_after and date_before:
            queryset = queryset.filter(created_date__gte=date_after, created_date__lte=date_before)
        elif date_after:
            queryset = queryset.filter(created_date__gte=date_after)
        elif date_before:
            queryset = queryset.filter(created_date__lte=date_before)
        if sort_by_price_asc:
            queryset = queryset.order_by('price', '-created_date')
        elif sort_by_price_desc:
            queryset = queryset.order_by('-price', '-created_date')

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class HouseForRentRetrieveView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    View to display available house details to buyer
    """
    queryset = House.objects.filter(is_available=True).filter(selling_choice="Rent")
    serializer_class = HouseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class HouseForRentListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to display available house list to buyer
    """

    serializer_class = HouseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        sort_by_price_asc = request.GET.get('sort_by_price_asc')
        sort_by_price_desc = request.GET.get('sort_by_price_desc')
        filter_city = request.GET.get('filter_city')
        filter_state = request.GET.get('filter_state')
        filter_amenities = request.GET.get('filter_amenities')
        filter_no_of_bedrooms = request.GET.get('filter_no_of_bedrooms')
        filter_possession = request.GET.get('filter_possession')
        filter_project_status = request.GET.get('filter_project_status')
        date_before = request.GET.get('date_before')
        date_after = request.GET.get('date_after')
        queryset = House.objects.filter(is_available=True).filter(selling_choice="Rent")

        if filter_city:
            queryset = queryset.filter(city=filter_city).order_by('-created_date')
        if filter_state:
            queryset = queryset.filter(state=filter_state).order_by('-created_date')
        if filter_amenities:
            queryset = queryset.filter(amenities=filter_amenities).order_by('-created_date')
        if filter_no_of_bedrooms:
            queryset = queryset.filter(no_of_bedrooms=filter_no_of_bedrooms).order_by('-created_date')
        if filter_possession:
            queryset = queryset.filter(possession=filter_possession).order_by('-created_date')
        if filter_project_status:
            queryset = queryset.filter(project_status=filter_project_status).order_by('-created_date')
        if search:
            queryset = queryset.filter(Q(city__contains=search) | Q(state__contains=search)).order_by('-created_date')
        if price_min and price_max:
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
        elif price_max:
            queryset = queryset.filter(price__lte=price_max)
        elif price_min:
            queryset = queryset.filter(price__gte=price_min)
        if date_after and date_before:
            queryset = queryset.filter(created_date__gte=date_after, created_date__lte=date_before)
        elif date_after:
            queryset = queryset.filter(created_date__gte=date_after)
        elif date_before:
            queryset = queryset.filter(created_date__lte=date_before)
        if sort_by_price_asc:
            queryset = queryset.order_by('price', '-created_date')
        elif sort_by_price_desc:
            queryset = queryset.order_by('-price', '-created_date')

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class FavouritesByUser(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    View to display all the shortlisted house to user
    """
    serializer_class = MyFavouritesSerializer
    lookup_field = 'user'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        favs = FavouritesUser.objects.filter(user=request.user.id)
        favourites_data = MyFavouritesSerializer(favs, many=True)
        return Response({'data': favourites_data.data}, status=status.HTTP_200_OK)
