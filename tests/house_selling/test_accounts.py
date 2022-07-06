import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    print("all users", User.objects.all())
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
    response = client.post(reverse('register'), payload)
    data = response.data['data']
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert data["phone_number"] == payload["phone_number"]
    assert data["address"] == payload["address"]
    assert "password" not in data
    assert "password2" not in data
    assert response.status_code == 201


@pytest.mark.django_db
def test_register_user_no_data():
    response = client.post(reverse('register'))
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_with_same_email(user):
    payload = {
        "first_name": "keya",
        "last_name": "patel",
        "username": "keya",
        "email": "dhwani@gmail.com",
        "phone_number": "+918670777787",
        "address": "ranip",
        "password": "Abcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'csscazgj')
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_with_same_username(user):
    payload = {
        "first_name": "keya",
        "last_name": "patel",
        "username": "dhwani",
        "email": "keya@gmail.com",
        "phone_number": "+918670777787",
        "address": "ranip",
        "password": "Abcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'sacszgj')
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_with_same_phone_number(user):
    payload = {
        "first_name": "keya",
        "last_name": "patel",
        "username": "keya",
        "email": "keya@gmail.com",
        "phone_number": "+918670777787",
        "address": "ranip",
        "password": "Abcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'zgzcsfsj')
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_invalid_password(user):
    payload = {
        "first_name": "keya",
        "last_name": "patel",
        "username": "keya",
        "email": "keya@gmail.com",
        "phone_number": "+918770777787",
        "address": "ranip",
        "password": "abcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'guuzgj')
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_confirmpsswd_psswd_not_match(user):
    payload = {
        "first_name": "keya",
        "last_name": "patel",
        "username": "keya",
        "email": "keya@gmail.com",
        "phone_number": "+918670977787",
        "address": "ranip",
        "password": "AAbcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'zgj')
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_invalid_username():
    payload = {
        "first_name": "dh",
        "last_name": "da",
        "username": "gf",
        "email": "dhwani@gmail.com",
        "phone_number": "+918670977787",
        "address": "gota",
        "password": "Abcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'bjhgak')
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_invalid_email():
    payload = {
        "first_name": "dh",
        "last_name": "da",
        "username": "dhwani",
        "email": "dhwanigmail.com",
        "phone_number": "+918670977787",
        "address": "gota",
        "password": "Abcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'aaaaaabjhgak')
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_invalid_phone_number():
    payload = {
        "first_name": "dh",
        "last_name": "da",
        "username": "dhwani",
        "email": "dhwani@gmail.com",
        "phone_number": "+91860977787",
        "address": "gota",
        "password": "Abcd@1234",
        "password2": "Abcd@1234"
    }
    response = client.post(reverse('register'), payload)
    print(response.data, 'rrrraaaaaabjhgak')
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user(user):
    login_data = {
        "email": "dhwani@gmail.com",
        "password": "Abcd@1234"
    }
    response = client.post(reverse('login'), login_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_with_no_data(user):
    response = client.post(reverse('login'))
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user_with_wrong_email(user):
    login_data = {
        "email": "dhwai@gmail.com",
        "password": "Abcd@1234"
    }
    response = client.post(reverse('login'), login_data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_login_user_with_wrong_password(user):
    login_data = {
        "email": "dhwani@gmail.com",
        "password": "AAbcd@1234"
    }
    response = client.post(reverse('login'), login_data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_login_user_with_wrong_username_and_password(user):
    login_data = {
        "email": "dhwai@gmail.com",
        "password": "AAbcd@1234"
    }
    response = client.post(reverse('login'), login_data)
    assert response.status_code == 404
