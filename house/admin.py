from django.contrib import admin
from house.models import Amenities, HouseReview, House, SiteReview, LikesUser, Likes

admin.site.register(Amenities)
admin.site.register(HouseReview)
admin.site.register(House)
admin.site.register(SiteReview)
admin.site.register(Likes)
admin.site.register(LikesUser)