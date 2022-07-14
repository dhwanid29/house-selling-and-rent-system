import pytest
from django.urls import reverse


class TestResendEmailUpdateLink:

    @pytest.mark.django_db
    def test_resend_link_with_invalid_email(self, authenticated_client):
        resend_link_data = {
            "email": "dhwanigmail.com",
        }
        response = authenticated_client.post(reverse('resend_email_update'), resend_link_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_resend_link_with_valid_email(self, authenticated_client):
        resend_link_data = {
            "email": "dhwani@gmail.com",
        }
        response = authenticated_client.post(reverse('resend_email_update'), resend_link_data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_resend_link_with_not_registered_email(self, authenticated_client):
        resend_link_data = {
            "email": "dhwanidadhich@gmail.com",
        }
        response = authenticated_client.post(reverse('resend_email_update'), resend_link_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_resend_link_with_no_data(self, authenticated_client):
        response = authenticated_client.post(reverse('resend_email_update'))
        assert response.status_code == 400