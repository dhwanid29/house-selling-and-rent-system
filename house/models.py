from django.db import models
from accounts.models import User


class Amenities(models.Model):
    """
    Model to create Amenities Table
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


POSSESSION_CHOICES = (
    ("Ready to Take", "Ready to Take"),
    ("Within 3 months", "Within 3 months"),
    ("Within 6 months", "Within 6 months"),
    ("Within 12 months", "Within 12 months"),
)

PROJECT_STATUS_CHOICES = (
    ("Under Construction", "Under Construction"),
    ("Constructed", "Constructed"),
)
BUY_OR_SELL_CHOICES = (
    ("Sell", "Sell"),
    ("Rent", "Rent"),
)


class House(models.Model):
    """
    Model to create House Table
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(Amenities)
    residence_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    no_of_bedrooms = models.IntegerField()
    no_of_lift = models.IntegerField()
    no_of_floors = models.IntegerField()
    no_of_building = models.IntegerField()
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    sqft = models.IntegerField()
    selling_choice = models.CharField(max_length=50, choices=BUY_OR_SELL_CHOICES, default="Sell")
    possession = models.CharField(max_length=50, choices=POSSESSION_CHOICES, default="Ready to Take")
    project_status = models.CharField(max_length=50, choices=PROJECT_STATUS_CHOICES, default="Constructed")
    is_available = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.residence_name


class HouseImages(models.Model):
    """
    Model to create HouseImages Table
    """
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_image_set')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    house_image = models.ImageField(upload_to='house_images/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.house_image


class HouseReview(models.Model):
    """
    Model to create HouseReview Table
    """
    house = models.ForeignKey(House, null=True, on_delete=models.CASCADE, related_name='house_review_set')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    review = models.TextField()
    created_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.review


class SiteReview(models.Model):
    """
    Model to create SiteReview Table
    """
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    review = models.TextField()
    created_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.review


class Likes(models.Model):
    """
    Model to Like House
    """
    user = models.ManyToManyField(User, through="LikesUser")
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.house


class LikesUser(models.Model):
    """
    Model to Like House
    """
    likes = models.ForeignKey(Likes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Favourites(models.Model):
    """
    Model to Add House to Favourites
    """
    user = models.ManyToManyField(User, through="FavouritesUser")
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class FavouritesUser(models.Model):
    """
    Model to Add House to Favourites
    """
    favourites = models.ForeignKey(Favourites, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    residence_name = models.CharField(max_length=255)
    no_of_bedrooms = models.IntegerField()
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    selling_choice = models.CharField(max_length=50, choices=BUY_OR_SELL_CHOICES, default="Sell")

    def __str__(self):
        return self.city
