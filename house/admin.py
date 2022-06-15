from django.contrib import admin
from house.models import Amenities, HouseReview, House, SiteReview

admin.site.register(Amenities)
admin.site.register(HouseReview)
admin.site.register(House)
admin.site.register(SiteReview)