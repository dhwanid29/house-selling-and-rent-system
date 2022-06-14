from django.db import models
from accounts.models import User


class Amenities(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HouseReview(models.Model):
    review = models.TextField()

    def __str__(self):
        return self.review


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


class House(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(Amenities)
    residence_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    no_of_bedrooms = models.IntegerField()
    no_of_lift = models.IntegerField()
    no_of_floors = models.IntegerField()
    no_of_building = models.IntegerField()
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    sqft = models.IntegerField()
    possession = models.CharField(max_length=50, choices=POSSESSION_CHOICES, default="Ready to Take")
    project_status = models.CharField(max_length=50, choices=PROJECT_STATUS_CHOICES, default="Constructed")
    created_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.residence_name


class HouseImages(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    house_image = models.ImageField(upload_to='house_images/')

    def __str__(self):
        return self.house_image