from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from accounts.models import User
from accounts.utils import EmailSend
from accounts.validations import validate_date, validate_price
from constants import NO_ACCESS_UPDATE_REVIEW, NO_ACCESS_UPDATE_HOUSE_IMAGE, DISLIKE_ERROR, LIKE_ERROR, FAVOURITE_ERROR, \
    REMOVE_FAVOURITES_ERROR, EMAIL_BODY_FAVOURITES, EMAIL_SUBJECT_FAVOURITES, NOT_REGISTERED, HOUSE_DOES_NOT_EXIST, \
    HOUSE_CREATED, HOUSE_UPDATED, REVIEW_CREATED, REVIEW_UPDATED, LIKED, UNLIKED, ADDED_TO_FAVOURITES, \
    REMOVED_FAVOURITES, PREFERENCE_CREATED, PREFERENCE_UPDATED, NO_ACCESS_UPDATE_PREFERENCE, DATA_RETRIEVED, \
    EMAIL_BODY_FAV_SELLER, EMAIL_SUBJECT_FAV_SELLER, AMENITIES_CREATED, AMENITIES_UPDATED, AMENITIES_VIEW, \
    AMENITIES_DELETE, REVIEW_ALREADY_CREATED, PREFERENCE_ALREADY_CREATED
from house.models import House, Amenities, HouseReview, SiteReview, HouseImages, Likes, LikesUser, Favourites, \
    FavouritesUser, Preference
from house.serializers import HouseSerializer, AmenitiesSerializer, HouseReviewSerializer, HouseReviewUpdateSerializer, \
    SiteReviewSerializer, SiteReviewUpdateSerializer, HouseImageSerializer, LikesSerializer, FavouritesSerializer, \
    MyFavouritesSerializer, HouseUpdateSerializer, HouseImageUpdateSerializer, PreferencesSerializer

header_token = openapi.Parameter('authorization', openapi.IN_HEADER, description="local header param",
                                 type=openapi.IN_HEADER)
city_param = openapi.Parameter('filter_city', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
state_param = openapi.Parameter('filter_state', in_=openapi.IN_QUERY, description='Description',
                                type=openapi.TYPE_STRING)
amenities_param = openapi.Parameter('filter_amenities', in_=openapi.IN_QUERY, description='Description',
                                    type=openapi.TYPE_STRING)
no_of_bedrooms_param = openapi.Parameter('filter_no_of_bedrooms', in_=openapi.IN_QUERY, description='Description',
                                         type=openapi.TYPE_STRING)
possession_param = openapi.Parameter('filter_possession', in_=openapi.IN_QUERY, description='Description',
                                     type=openapi.TYPE_STRING)
project_status_param = openapi.Parameter('filter_project_status', in_=openapi.IN_QUERY, description='Description',
                                         type=openapi.TYPE_STRING)
date_before_param = openapi.Parameter('date_before', in_=openapi.IN_QUERY, description='Description',
                                      type=openapi.TYPE_STRING)
date_after_param = openapi.Parameter('date_after', in_=openapi.IN_QUERY, description='Description',
                                     type=openapi.TYPE_STRING)
search_param = openapi.Parameter('search', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
price_min_param = openapi.Parameter('price_min', in_=openapi.IN_QUERY, description='Description',
                                    type=openapi.TYPE_STRING)
price_max_param = openapi.Parameter('price_max', in_=openapi.IN_QUERY, description='Description',
                                    type=openapi.TYPE_STRING)
sort_by_price_asc_param = openapi.Parameter('sort_by_price_asc', in_=openapi.IN_QUERY, description='Description',
                                            type=openapi.TYPE_STRING)
sort_by_price_desc_param = openapi.Parameter('sort_by_price_desc', in_=openapi.IN_QUERY, description='Description',
                                             type=openapi.TYPE_STRING)


class AmenitiesCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    View to add, update, delete Amenities
    """
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(manual_parameters=[header_token])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': AMENITIES_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)


class AmenitiesUpdateDelete(generics.GenericAPIView, mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    """
    View to update, delete Amenities
    """
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    @swagger_auto_schema(manual_parameters=[header_token])
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AmenitiesSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'data': serializer.data, 'msg': AMENITIES_UPDATED}, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[header_token])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'msg': AMENITIES_DELETE}, status=status.HTTP_204_NO_CONTENT)


class AmenitiesViewList(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to view Amenities
    """
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data, 'msg': AMENITIES_VIEW}, status=status.HTTP_200_OK)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='destroy', decorator=swagger_auto_schema(manual_parameters=[header_token]))
class HouseViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete House Details
    """
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(manual_parameters=[header_token])
    def create(self, request, *args, **kwargs):
        get_sellers = House.objects.filter(user=request.user.id)
        if get_sellers:
            get_fav_houses = []
            for i in get_sellers:
                query = Favourites.objects.filter(house=i.id).first()
                if query:
                    get_fav_houses.append(query.id)
            queryset = FavouritesUser.objects.filter(favourites__in=get_fav_houses).distinct('user')

            for i in queryset:
                user_email = User.objects.filter(username=i).first()
                # Send Mail
                data = {
                    'subject': EMAIL_SUBJECT_FAV_SELLER,
                    'body': EMAIL_BODY_FAV_SELLER,
                    'to_email': user_email
                }
                EmailSend.send_email(data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': HOUSE_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)

    @swagger_auto_schema(manual_parameters=[header_token])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            serializer = HouseUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

            return Response({'data': serializer.data, 'msg': HOUSE_UPDATED}, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_REVIEW}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='destroy', decorator=swagger_auto_schema(manual_parameters=[header_token]))
class SiteReviewViewSet(viewsets.ModelViewSet):
    """
    View to add, get, update, delete Site Review by id
    """
    serializer_class = SiteReviewSerializer
    queryset = SiteReview.objects.all()
    lookup_field = 'user'
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(manual_parameters=[header_token])
    def create(self, request, *args, **kwargs):
        get_user = SiteReview.objects.filter(user=request.user.id).first()
        if get_user:
            return Response({'msg': REVIEW_ALREADY_CREATED}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': REVIEW_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)

    @swagger_auto_schema(manual_parameters=[header_token])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            serializer = SiteReviewUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

            return Response({'data': serializer.data, 'msg': REVIEW_UPDATED}, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_REVIEW}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='destroy', decorator=swagger_auto_schema(manual_parameters=[header_token]))
class HouseReviewViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete House Review
    """
    serializer_class = HouseReviewSerializer
    queryset = HouseReview.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(manual_parameters=[header_token])
    def create(self, request, *args, **kwargs):
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house).first()
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        get_user = HouseReview.objects.filter(user=request.user.id, house=find_house.id).first()
        if get_user:
            return Response({'msg': REVIEW_ALREADY_CREATED}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': REVIEW_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)

    @swagger_auto_schema(manual_parameters=[header_token])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            get_house = request.data.get('house')
            find_house = House.objects.filter(id=get_house).first()
            if not find_house:
                return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
            serializer = HouseReviewUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

            return Response({'data': serializer.data, 'msg': REVIEW_UPDATED}, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_REVIEW}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='destroy', decorator=swagger_auto_schema(manual_parameters=[header_token]))
class HouseImageViewSet(viewsets.ModelViewSet):
    """
    View to get, update, delete House Image
    """
    serializer_class = HouseImageSerializer
    queryset = HouseImages.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(manual_parameters=[header_token])
    def create(self, request, *args, **kwargs):
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house)
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': HOUSE_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)

    @swagger_auto_schema(manual_parameters=[header_token])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            request.data['house'] = instance.house.id
            serializer = HouseImageUpdateSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response({'data': serializer.data, 'msg': HOUSE_UPDATED}, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_HOUSE_IMAGE}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[header_token]))
class LikesViewSet(viewsets.ModelViewSet):
    """
    View to Like and Dislike House
    """
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    lookup_field = 'house'
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    @swagger_auto_schema(manual_parameters=[header_token])
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

    @swagger_auto_schema(manual_parameters=[header_token])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house)
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        house_obj = House.objects.get(pk=request.data.get('house'))
        liked_user = Likes.objects.filter(house=instance.house.id).values('user')
        for user in liked_user:
            if user['user'] == request.user.id:
                instance.user.remove(request.user)
                all_likes = Likes.objects.get(house=house_obj)
                serializer = self.get_serializer(all_likes, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save(house=house_obj)
                return Response({'data': serializer.data, 'msg': UNLIKED}, status=status.HTTP_200_OK)
        return Response({'msg': DISLIKE_ERROR}, status=status.HTTP_204_NO_CONTENT)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[header_token]))
class FavouritesViewSet(viewsets.ModelViewSet):
    """
    View to Shortlist House and remove House from Shortlisted list
    """
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer
    lookup_field = 'house'
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    @swagger_auto_schema(manual_parameters=[header_token])
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
            except user.DoesNotExist:
                return Response({'msg': NOT_REGISTERED}, status=status.HTTP_404_NOT_FOUND)
            all_favourites = Favourites.objects.get(house=house_obj)
            serializer = FavouritesSerializer(all_favourites, many=False)

            return Response({'data': serializer.data, 'msg': ADDED_TO_FAVOURITES}, status=status.HTTP_201_CREATED)
        return Response({'msg': FAVOURITE_ERROR}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[header_token])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        get_house = request.data.get('house')
        find_house = House.objects.filter(id=get_house)
        if not find_house:
            return Response({'msg': HOUSE_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        house_obj = House.objects.get(pk=request.data.get('house'))
        favourited_user = Favourites.objects.filter(house=instance.house.id).values('user')
        for user in favourited_user:
            if user['user'] == request.user.id:
                instance.user.remove(request.user)
                all_favourites = Favourites.objects.get(house=house_obj)
                serializer = self.get_serializer(all_favourites, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save(house=house_obj)
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

    @swagger_auto_schema(manual_parameters=[header_token])
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data, 'msg': DATA_RETRIEVED}, status=status.HTTP_200_OK)


class BuyerHouseListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to display available house list to buyer
    """
    serializer_class = HouseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[header_token, city_param, state_param, amenities_param,
                                            no_of_bedrooms_param, possession_param, project_status_param,
                                            date_before_param,
                                            date_after_param, search_param, price_min_param, price_max_param,
                                            sort_by_price_asc_param,
                                            sort_by_price_desc_param])
    def get(self, request, *args, **kwargs):
        queryset = House.objects.filter(is_available=True).filter(selling_choice="Sell")
        search = request.GET.get('search')
        price_min = request.GET.get('price_min')
        if price_min:
            validate_price(price_min)
        price_max = request.GET.get('price_max')
        if price_max:
            validate_price(price_max)
        sort_by_price_asc = request.GET.get('sort_by_price_asc')
        sort_by_price_desc = request.GET.get('sort_by_price_desc')
        filter_city = request.GET.get('filter_city')
        filter_state = request.GET.get('filter_state')
        filter_amenities = request.GET.get('filter_amenities')
        filter_no_of_bedrooms = request.GET.get('filter_no_of_bedrooms')
        filter_possession = request.GET.get('filter_possession')
        filter_project_status = request.GET.get('filter_project_status')
        date_before = request.GET.get('date_before')
        if date_before:
            validate_date(date_before)
        date_after = request.GET.get('date_after')
        if date_after:
            validate_date(date_after)
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
        return Response({'data': serializer.data, 'msg': DATA_RETRIEVED}, status=status.HTTP_200_OK)


class HouseForRentRetrieveView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    View to display available house details to buyer
    """
    queryset = House.objects.filter(is_available=True).filter(selling_choice="Rent")
    serializer_class = HouseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[header_token])
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data, 'msg': DATA_RETRIEVED}, status=status.HTTP_200_OK)


class HouseForRentListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to display available house list to buyer
    """

    serializer_class = HouseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[header_token, city_param, state_param, amenities_param,
                                            no_of_bedrooms_param, possession_param, project_status_param,
                                            date_before_param,
                                            date_after_param, search_param, price_min_param, price_max_param,
                                            sort_by_price_asc_param,
                                            sort_by_price_desc_param])
    def get(self, request, *args, **kwargs):
        queryset = House.objects.filter(is_available=True).filter(selling_choice="Rent")
        search = request.GET.get('search')
        price_min = request.GET.get('price_min')
        if price_min:
            validate_price(price_min)
        price_max = request.GET.get('price_max')
        if price_max:
            validate_price(price_max)
        sort_by_price_asc = request.GET.get('sort_by_price_asc')
        sort_by_price_desc = request.GET.get('sort_by_price_desc')
        filter_city = request.GET.get('filter_city')
        filter_state = request.GET.get('filter_state')
        filter_amenities = request.GET.get('filter_amenities')
        filter_no_of_bedrooms = request.GET.get('filter_no_of_bedrooms')
        filter_possession = request.GET.get('filter_possession')
        filter_project_status = request.GET.get('filter_project_status')
        date_before = request.GET.get('date_before')
        if date_before:
            validate_date(date_before)
        date_after = request.GET.get('date_after')
        if date_after:
            validate_date(date_after)

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
        return Response({'data': serializer.data, 'msg': DATA_RETRIEVED}, status=status.HTTP_200_OK)


class FavouritesByUser(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    View to display all the shortlisted house to user
    """
    serializer_class = MyFavouritesSerializer
    lookup_field = 'user'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[header_token])
    def get(self, request, *args, **kwargs):
        favs = FavouritesUser.objects.filter(user=request.user.id)
        favourites_data = MyFavouritesSerializer(favs, many=True)
        return Response({'data': favourites_data.data, 'msg': DATA_RETRIEVED}, status=status.HTTP_200_OK)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[header_token]))
@method_decorator(name='destroy', decorator=swagger_auto_schema(manual_parameters=[header_token]))
class PreferencesViewSet(viewsets.ModelViewSet):
    """
    View to insert, update, view and delete preferences
    """
    serializer_class = PreferencesSerializer
    queryset = Preference.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(manual_parameters=[header_token])
    def create(self, request, *args, **kwargs):
        get_user = Preference.objects.filter(user=request.user.id).first()
        if get_user:
            return Response({'msg': PREFERENCE_ALREADY_CREATED}, status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'msg': PREFERENCE_CREATED}, status=status.HTTP_201_CREATED,
                        headers=headers)

    @swagger_auto_schema(manual_parameters=[header_token])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.id == request.user.id:
            serializer = PreferencesSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'data': serializer.data, 'msg': PREFERENCE_UPDATED}, status=status.HTTP_200_OK)
        return Response({'msg': NO_ACCESS_UPDATE_PREFERENCE}, status=status.HTTP_400_BAD_REQUEST)


class RecommendedHousesListView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to display Recommended Houses to users according to their preferences
    """
    serializer_class = PreferencesSerializer
    lookup_field = 'user'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[header_token])
    def get(self, request, *args, **kwargs):
        get_user_preference = Preference.objects.filter(user=request.user.id).first()
        recommendations = House.objects.filter(residence_name=get_user_preference.residence_name,
                                               no_of_bedrooms=get_user_preference.no_of_bedrooms,
                                               state=get_user_preference.state,
                                               city=get_user_preference.city,
                                               selling_choice=get_user_preference.selling_choice)
        house_data = HouseSerializer(recommendations, many=True)
        return Response({'data': house_data.data, 'msg': DATA_RETRIEVED}, status=status.HTTP_200_OK)


class TrendingHousesView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    View to display trending houses to users(Most Liked Houses)
    """
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[header_token])
    def get(self, request, *args, **kwargs):
        trending_houses_dict = {}
        rec = Likes.objects.all()
        for i in rec:
            get_trendy_houses = LikesUser.objects.filter(likes=i.id).annotate(liked_houses=Count('likes')).order_by(
                'liked_houses')
            trending_houses_dict[i.house.id] = len(get_trendy_houses)
        trendy_houses = dict(sorted(trending_houses_dict.items(), key=lambda item: item[1], reverse=True)).keys()
        trending_houses_list = list(trendy_houses)
        queryset = House.objects.filter(id__in=trending_houses_list)
        query = sorted(queryset, key=lambda i: trending_houses_list.index(i.id))
        house_data = HouseSerializer(query, many=True)
        return Response({'data': house_data.data, 'msg': DATA_RETRIEVED}, status=status.HTTP_200_OK)
