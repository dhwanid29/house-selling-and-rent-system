from django.urls import path
from house.views import AmenitiesView, AddAmenities, HouseReviewViewSet, SiteReviewViewSet, AddHouse, HouseView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('house_review', HouseReviewViewSet, basename='house_review'),
router.register('site_review', SiteReviewViewSet, basename='site_review')

urlpatterns = [
    path('add_house/', AddHouse.as_view(), name='add_house'),
    path('detail/<int:id>/', HouseView.as_view(), name='house_details'),
    path('add_amenities/', AddAmenities.as_view(), name="add_amenities"),
    path('amenities/<int:id>/', AmenitiesView.as_view(), name="amenities"),
] + router.urls