from django.urls import path
from house.views import HouseReviewViewSet, SiteReviewViewSet, \
    HouseImageViewSet, HouseViewSet, LikesViewSet, FavouritesViewSet, BuyerHouseListView, BuyerHouseRetrieveView, \
    FavouritesByUser, HouseForRentListView, HouseForRentRetrieveView, PreferencesViewSet, RecommendedHousesListView, \
    TrendingHousesView, AmenitiesViewList, AmenitiesUpdateDelete, AmenitiesCreate
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('house_review', HouseReviewViewSet, basename='house_review')
router.register('site_review', SiteReviewViewSet, basename='site_review')
router.register('house_detail', HouseViewSet, basename='house_detail')
router.register('house_images', HouseImageViewSet, basename='house_images')
router.register('likes', LikesViewSet, basename='likes')
router.register('favourites', FavouritesViewSet, basename='favourites')
router.register('preferences', PreferencesViewSet, basename='preferences')


urlpatterns = [
    path('view_amenities/', AmenitiesViewList.as_view(), name="view_amenities"),
    path('amenities/', AmenitiesCreate.as_view(), name="add_amenities"),
    path('amenities/<int:id>/', AmenitiesUpdateDelete.as_view(), name="amenities_update"),
    path('available_houses/', BuyerHouseListView.as_view(), name="available_houses"),
    path('available_houses/<int:id>/', BuyerHouseRetrieveView.as_view(), name="available_houses"),
    path('my_favourites/<int:user>/', FavouritesByUser.as_view(), name="my_favourites"),
    path('available_for_rent/', HouseForRentListView.as_view(), name="available_for_rent"),
    path('available_for_rent/<int:id>/', HouseForRentRetrieveView.as_view(), name="available_for_rent_detail"),
    path('recommended_houses/<int:user>/', RecommendedHousesListView.as_view(), name="recommended_houses"),
    path('trending_houses/', TrendingHousesView.as_view(), name="trending_houses"),
] + router.urls

