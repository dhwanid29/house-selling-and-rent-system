import pytest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework.test import APIClient
from accounts.models import User

client = APIClient()


class TestSendPasswordEmail:

    @pytest.mark.django_db
    def test_send_password_email_with_invalid_email(self):
        send_password_email_data = {
            "email": "dhwanigmail.com",
        }
        response = client.post(reverse('send-reset-password-email'), send_password_email_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_send_password_email_with_valid_email(self, registered_user):
        send_password_email_data = {
            "email": "dhwani@gmail.com",
        }
        response = registered_user.post(reverse('send-reset-password-email'), send_password_email_data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_send_password_email_with_not_registered_email(self):
        send_password_email_data = {
            "email": "dhwanidadhich@gmail.com",
        }
        response = client.post(reverse('send-reset-password-email'), send_password_email_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_send_password_email_with_no_data(self):
        response = client.post(reverse('send-reset-password-email'))
        assert response.status_code == 400


class TestResetUserPassword:

    @pytest.mark.django_db
    def test_reset_password_with_valid_password(self, create_user):
        reset_password_data = {
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        user_email = User.objects.get(email=create_user.email)
        uid = urlsafe_base64_encode(force_bytes(str(user_email.id)))
        token = PasswordResetTokenGenerator().make_token(user_email)
        response = client.post(reverse('reset-password', kwargs={'uid': uid, 'token': token}), reset_password_data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_reset_password_with_invalid_password(self, create_user):
        reset_password_data = {
            "password": "abcd@1234",
            "password2": "Abcd@1234"
        }
        user_email = User.objects.get(email=create_user.email)
        uid = urlsafe_base64_encode(force_bytes(str(user_email.id)))
        token = PasswordResetTokenGenerator().make_token(user_email)
        response = client.post(reverse('reset-password', kwargs={'uid': uid, 'token': token}), reset_password_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_reset_password_with_psswd_and_confirmpsswd_not_match(self, create_user):
        reset_password_data = {
            "password": "Abcd@1234",
            "password2": "AAbcd@1234"
        }
        user_email = User.objects.get(email=create_user.email)
        uid = urlsafe_base64_encode(force_bytes(str(user_email.id)))
        token = PasswordResetTokenGenerator().make_token(user_email)
        response = client.post(reverse('reset-password', kwargs={'uid': uid, 'token': token}), reset_password_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_reset_password_with_no_data(self, create_user):
        user_email = User.objects.get(email=create_user.email)
        uid = urlsafe_base64_encode(force_bytes(str(user_email.id)))
        token = PasswordResetTokenGenerator().make_token(user_email)
        response = client.post(reverse('reset-password', kwargs={'uid': uid, 'token': token}))
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_reset_password_with_no_password(self, create_user):
        reset_password_data = {
            "password2": "AAbcd@1234"
        }
        user_email = User.objects.get(email=create_user.email)
        uid = urlsafe_base64_encode(force_bytes(str(user_email.id)))
        token = PasswordResetTokenGenerator().make_token(user_email)
        response = client.post(reverse('reset-password', kwargs={'uid': uid, 'token': token}), reset_password_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_reset_password_with_no_confirm_password(self, create_user):
        reset_password_data = {
            "password": "Abcd@1234"
        }
        user_email = User.objects.get(email=create_user.email)
        uid = urlsafe_base64_encode(force_bytes(str(user_email.id)))
        token = PasswordResetTokenGenerator().make_token(user_email)
        response = client.post(reverse('reset-password', kwargs={'uid': uid, 'token': token}), reset_password_data)
        assert response.status_code == 400

