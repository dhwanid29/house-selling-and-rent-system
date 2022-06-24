from django.urls import path
from house.views import AmenitiesView, AddAmenities, HouseReviewViewSet, SiteReviewViewSet, \
    HouseImageViewSet, HouseViewSet, LikesViewSet, FavouritesViewSet, BuyerHouseListView, BuyerHouseRetrieveView, \
    FavouritesByUser, HouseForRentListView, HouseForRentRetrieveView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('house_review', HouseReviewViewSet, basename='house_review')
router.register('site_review', SiteReviewViewSet, basename='site_review')
router.register('house_detail', HouseViewSet, basename='house_detail')
router.register('house_images', HouseImageViewSet, basename='house_images')
router.register('likes', LikesViewSet, basename='likes')
router.register('favourites', FavouritesViewSet, basename='favourites')


urlpatterns = [
    path('add_amenities/', AddAmenities.as_view(), name="add_amenities"),
    path('amenities/<int:id>/', AmenitiesView.as_view(), name="amenities"),
    path('available_houses/', BuyerHouseListView.as_view(), name="available_houses"),
    path('available_houses/<int:id>/', BuyerHouseRetrieveView.as_view(), name="available_houses"),
    path('my_favourites/<int:user>/', FavouritesByUser.as_view(), name="my_favourites"),
    path('available_for_rent/', HouseForRentListView.as_view(), name="available_for_rent"),
    path('available_for_rent/<int:id>/', HouseForRentRetrieveView.as_view(), name="available_for_rent_detail"),
] + router.urls

