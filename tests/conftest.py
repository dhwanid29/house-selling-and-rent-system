import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User


@pytest.fixture
def create_user():
    client = APIClient()
    user, created = User.objects.get_or_create(first_name="dhwani", last_name="dadhich", username="dhwani",
                                               email="dhwani@gmail.com",
                                               phone_number="+918670777787", address="gota")
    if created:
        print(f'total users in database: {User.objects.all().count()}')
        print(f'saving user password for user pk: {user.pk}')
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
        "password2": "Abcd@1234"
    }
    res = client.post(reverse('register'), payload)
    return client

@pytest.fixture
def authenticated_client(create_user):
    client = APIClient()
    print(f'users password is: {create_user.password}')
    res = client.post(reverse('login'), {"email": create_user.email, "password": "Abcd@1234"})
    print(f'response data in fixture is: {res.data}')
    get_token = res.data['token']
    token = get_token['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


#
# client = APIClient()
#
# @pytest.fixture
# def user():
#     # user_data = {
#     #     "first_name": "dhwani",
#     #     "last_name": "dadhich",
#     #     "username": "dhwani",
#     #     "email": "dhwani@gmail.com",
#     #     "phone_number": "+918670777787",
#     #     "address": "gota",
#     #     "password": "Abcd@1234",
#     #     "password2": "Abcd@1234"
#     # }
#     user = User.objects.create(first_name="dhwani", last_name="dadhich", username="dhwani", email="dhwani@gmail.com",
#                                phone_number="+918670777787", address="gota")
#     user.set_password(raw_password='Abcd@1234')
#     user.save()
#     print('sjdbj', user)
#     return user
#
#
# @pytest.fixture
# def authorized_user(user):
#     res = client.post(reverse('login'), {"email": user.email, "password": "Abcd@1234"})
#     get_token = res.data['token']
#     token = get_token['access']
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
#     print(token, 'tokennnnnnnnnn-------------------------------------------')
#     return token


