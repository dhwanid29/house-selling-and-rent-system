import pytest
from django.urls import reverse
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user(self):
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

    def test_register_user_no_data(self):
        response = client.post(reverse('register'))
        assert response.status_code == 400

    def test_register_user_with_same_email(self, registered_user):
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
        response = registered_user.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_with_same_username(self, registered_user):
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
        response = registered_user.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_with_same_phone_number(self, registered_user):
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
        response = registered_user.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_invalid_password(self):
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
        assert response.status_code == 400

    def test_register_user_confirmpsswd_psswd_not_match(self):
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
        assert response.status_code == 400

    def test_register_user_invalid_username(self):
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
        assert response.status_code == 400

    def test_register_user_invalid_email(self):
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
        assert response.status_code == 400

    def test_register_user_invalid_phone_number(self):
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
        assert response.status_code == 400

    def test_register_user_no_first_name(self):
        payload = {
            "last_name": "patel",
            "username": "keya",
            "email": "keya@gmail.com",
            "phone_number": "+918670977787",
            "address": "ranip",
            "password": "AAbcd@1234",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_no_last_name(self):
        payload = {
            "first_name": "keya",
            "username": "keya",
            "email": "keya@gmail.com",
            "phone_number": "+918670977787",
            "address": "ranip",
            "password": "AAbcd@1234",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_no_username(self):
        payload = {
            "first_name": "keya",
            "last_name": "patel",
            "email": "keya@gmail.com",
            "phone_number": "+918670977787",
            "address": "ranip",
            "password": "AAbcd@1234",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_no_email(self):
        payload = {
            "first_name": "keya",
            "last_name": "patel",
            "username": "keya",
            "phone_number": "+918670977787",
            "address": "ranip",
            "password": "AAbcd@1234",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_no_password(self):
        payload = {
            "first_name": "keya",
            "last_name": "patel",
            "username": "keya",
            "phone_number": "+918670977787",
            "address": "ranip",
            "email": "keya@gmail.com",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_no_confirm_password(self):
        payload = {
            "first_name": "keya",
            "last_name": "patel",
            "username": "keya",
            "phone_number": "+918670977787",
            "address": "ranip",
            "email": "keya@gmail.com",
            "password": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_no_phone_number(self):
        payload = {
            "first_name": "keya",
            "last_name": "patel",
            "username": "keya",
            "address": "ranip",
            "email": "keya@gmail.com",
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    def test_register_user_no_address(self):
        payload = {
            "first_name": "keya",
            "last_name": "patel",
            "username": "keya",
            "phone_number": "+918670977787",
            "email": "keya@gmail.com",
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400


@pytest.mark.django_db
class TestUserLogin:

    def test_login_user(self, create_user):
        login_data = {
            "email": "dhwani@gmail.com",
            "password": "Abcd@1234"
        }
        response = client.post(reverse('login'), login_data)
        assert response.status_code == 200

    def test_login_user_with_no_data(self, create_user):
        response = client.post(reverse('login'))
        assert response.status_code == 404

    def test_login_user_with_wrong_email(self, create_user):
        login_data = {
            "email": "dhwai@gmail.com",
            "password": "Abcd@1234"
        }
        response = client.post(reverse('login'), login_data)
        assert response.status_code == 404

    def test_login_user_with_wrong_password(self, create_user):
        login_data = {
            "email": "dhwani@gmail.com",
            "password": "AAbcd@1234"
        }
        response = client.post(reverse('login'), login_data)
        assert response.status_code == 404

    def test_login_user_with_wrong_username_and_password(self, create_user):
        login_data = {
            "email": "dhwai@gmail.com",
            "password": "AAbcd@1234"
        }
        response = client.post(reverse('login'), login_data)
        assert response.status_code == 404

    def test_login_user_with_invalid_email(self, create_user):
        login_data = {
            "email": "dhwaigmail.com",
            "password": "AAbcd@1234"
        }
        response = client.post(reverse('login'), login_data)
        assert response.status_code == 404

    def test_login_user_with_no_email(self, create_user):
        login_data = {
            "password": "Abcd@1234"
        }
        response = client.post(reverse('login'), login_data)
        assert response.status_code == 404

    def test_login_user_with_no_password(self, create_user):
        login_data = {
            "email": "dhwani@gmail.com",
        }
        response = client.post(reverse('login'), login_data)
        assert response.status_code == 404