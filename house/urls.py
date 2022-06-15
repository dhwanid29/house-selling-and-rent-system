from django.urls import path
from house.views import HouseView, AddHouse, AmenitiesView, AddAmenities, HouseReviewViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('house_review', HouseReviewViewSet, basename='house_review')

urlpatterns = [
    path('add_house/', AddHouse.as_view(), name='add_house'),
    path('detail/<int:id>/', HouseView.as_view(), name='house_details'),
    path('add_amenities/', AddAmenities.as_view(), name="add_amenities"),
    path('amenities/<int:id>/', AmenitiesView.as_view(), name="amenities"),
    # path('house_review/', HouseReviewViewSet.as_view(), name='add_house_review')
] + router.urls