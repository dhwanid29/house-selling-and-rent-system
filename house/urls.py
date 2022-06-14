from django.urls import path
from house.views import HouseView, AddHouse, AmenitiesView, AddAmenities

urlpatterns = [
    path('add_house/', AddHouse.as_view(), name='add_house'),
    path('detail/<int:id>/', HouseView.as_view(), name='house_details'),
    path('add_amenities/', AddAmenities.as_view(), name="add_amenities"),
    path('amenities/<int:id>/', AmenitiesView.as_view(), name="amenities"),
    # path('add_house_review/', HouseReviewView.as_view(), name='add_house_review')
]