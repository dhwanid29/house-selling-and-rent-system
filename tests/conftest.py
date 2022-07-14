import pytest
from django.contrib.auth.tokens import default_token_generator
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework.test import APIClient
from accounts.models import User
from house.models import House, Amenities, HouseReview, SiteReview, Likes, Favourites, Preference, HouseImages


@pytest.fixture
def create_user():
    client = APIClient()
    user, created = User.objects.get_or_create(first_name="dhwani", last_name="dadhich", username="dhwani",
                                               email="dhwani@gmail.com",
                                               phone_number="+918670777787", address="gota", is_admin=True)
    if created:
        user.set_password(raw_password='Abcd@1234')
        user.save()
    return user


@pytest.fixture
def registered_user():
    client = APIClient()
    payload = {
        "first_name": "dhwani",
        "last_name": "dadhich",
        "username": "dhwani",
        "email": "dhwani@gmail.com",
        "phone_number": "+918670777787",
        "address": "gota",
        "password": "Abcd@1234",
        "password2": "Abcd@1234",
    }
    res = client.post(reverse('register'), payload)
    return client


@pytest.fixture
def authenticated_client(create_user):
    client = APIClient()
    res = client.post(reverse('login'), {"email": create_user.email, "password": "Abcd@1234"})
    get_user = User.objects.filter(email=create_user.email).first()
    pytest.user_id = get_user.id
    get_token = res.data['token']
    token = get_token['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def create_house_amenities(authenticated_client):
    amenities_add, created = Amenities.objects.get_or_create(name="Garden")
    amenities_add.save()
    get_amenities = Amenities.objects.filter(name="Garden").first()
    pytest.amenities = get_amenities.id
    return get_amenities


@pytest.fixture
def create_house(authenticated_client):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    amenities_add, created = Amenities.objects.get_or_create(name="Garden")
    amenities_add.save()
    get_amenities = Amenities.objects.filter(name="Garden").first()
    house, created = House.objects.get_or_create(
            residence_name = "shayona green",
            price = "20000",
            no_of_bedrooms = "3",
            no_of_lift = "2",
            no_of_floors = "5",
            no_of_building = "13",
            state = "gujarat",
            city = "ahmedabad",
            sqft = "1500",
            possession = "Within 6 months",
            selling_choice = "Sell",
            address = "gota",
            project_status = "Constructed",
            user = instance
    )
    if created:
        house.amenities.add(get_amenities.id)
        house.save()
    get_house = House.objects.first()
    pytest.house_id = get_house.id
    return house


@pytest.fixture
def create_house_rent(authenticated_client):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    amenities_add, created = Amenities.objects.get_or_create(name="Garden")
    amenities_add.save()
    get_amenities = Amenities.objects.filter(name="Garden").last()
    house, created = House.objects.get_or_create(
            residence_name = "shayona green",
            price = "22498",
            no_of_bedrooms = "3",
            no_of_lift = "2",
            no_of_floors = "5",
            no_of_building = "13",
            state = "gujarat",
            city = "ahmedabad",
            sqft = "1500",
            possession = "Within 6 months",
            selling_choice = "Rent",
            address = "gota",
            project_status = "Constructed",
            user = instance
    )
    if created:
        house.amenities.add(get_amenities.id)
        house.save()
    get_house = House.objects.first()
    pytest.house_id = get_house.id
    return house


@pytest.fixture
def create_house_review(authenticated_client, create_house):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    get_house =  pytest.house_id
    house_instance = House.objects.get(id=get_house)
    house_review, created = HouseReview.objects.get_or_create(
            house = house_instance,
            review = "good",
            user = instance
    )
    house_review.save()
    get_house_review = HouseReview.objects.first()
    pytest.house_review_id = get_house_review.id
    return house_review


@pytest.fixture
def create_site_review(authenticated_client):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    site_review, created = SiteReview.objects.get_or_create(
            review = "good",
            user = instance
    )
    site_review.save()
    get_site_review = SiteReview.objects.first()
    pytest.site_review_id = get_site_review.id
    return site_review


@pytest.fixture
def create_house_like(authenticated_client, create_house):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    get_house = pytest.house_id
    house_instance = House.objects.get(id=get_house)
    like, created = Likes.objects.get_or_create(house=house_instance)
    like.user.add(instance)
    like.save()
    return like


@pytest.fixture
def create_house_favourites(authenticated_client, create_house):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    get_house = pytest.house_id
    house_instance = House.objects.get(id=get_house)
    fav, created = Favourites.objects.get_or_create(house=house_instance)
    fav.user.add(instance)
    fav.save()
    return fav


@pytest.fixture
def create_preference(authenticated_client):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    preference, created = Preference.objects.get_or_create(
            residence_name = "shayona green",
            no_of_bedrooms = "2",
            state = "gujarat",
            city = "ahmedabad",
            selling_choice = "Sell",
            user = instance
    )
    preference.save()
    get_preference = Preference.objects.first()
    pytest.preference_id = get_preference.id
    return get_preference


@pytest.fixture
def create_house_images(authenticated_client, create_house):
    user_instance = pytest.user_id
    instance = User.objects.get(id=user_instance)
    get_house =  pytest.house_id
    house_instance = House.objects.get(id=get_house)
    image_data = File(open('media/default.jpg', 'rb'))
    image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')
    house_image, created = HouseImages.objects.get_or_create(
            house = house_instance,
            house_image = image,
            user = instance
    )
    house_image.save()
    get_house_image = HouseImages.objects.first()
    pytest.house_image_id = get_house_image.id
    return house_image


@pytest.fixture
def user_token(create_user):
    user_email = User.objects.filter(email=create_user.email).first()
    if user_email:
        pytest.uid = urlsafe_base64_encode(force_bytes(str(user_email.id)))
        pytest.token = default_token_generator.make_token(user_email)


