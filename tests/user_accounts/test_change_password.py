import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db(True)
class TestChangePassword:

    def test_change_password_with_invalid_password(self, authenticated_client):
        change_password_data = {
            "current_password": "Abcdfe@1235676574",
            "password": "Abc@1234",
            "password2": "Abc@1234"
        }

        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400

    def test_change_password_if_password_and_confirmpassword_not_match(self, authenticated_client):
        change_password_data = {
            "current_password": "Abcd@1234",
            "password": "Abcd@1234",
            "password2": "AAbcd@1234"
        }
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400

    def test_change_password_with_no_data(self, authenticated_client):
        response = authenticated_client.post(reverse('changepassword'))
        assert response.status_code == 400

    def test_change_password_with_not_registered_email(self, authenticated_client):
        change_password_data = {
            "email": "dhwanidadhich@gmail.com",
        }
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400

    def test_change_password_with_wrong_current_password(self, authenticated_client):
        change_password_data = {
            "current_password": "Abcd@12334",
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400

    def test_change_password_valid_data_but_same_old_psswd_and_new_psswd(self, authenticated_client):
        change_password_data = {
            "current_password": "Abcd@1234",
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        # headers = {}
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400

    def test_change_password_valid_data(self, authenticated_client):
        change_password_data = {
            "current_password": "Abcd@1234",
            "password": "Abcd@12345",
            "password2": "Abcd@12345"
        }
        # headers = {}
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 200

    def test_change_password_valid_data_but_unauthorized(self, create_user):
        change_password_data = {
            "current_password": "Abcd@1234",
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        response = APIClient().post(reverse('changepassword'), change_password_data)
        assert response.status_code == 401

    def test_change_password_with_no_password(self, authenticated_client):
        change_password_data = {
            "current_password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400

    def test_change_password_with_no_confirm_password(self, authenticated_client):
        change_password_data = {
            "current_password": "Abcd@1234",
            "password": "Abcd@1234"
        }
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400

    def test_change_password_with_no_current_password(self, authenticated_client):
        change_password_data = {
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        response = authenticated_client.post(reverse('changepassword'), change_password_data)
        assert response.status_code == 400
