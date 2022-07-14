import pytest
from django.urls import reverse


@pytest.mark.django_db(True)
class TestRentHouse:
    def test_rent_house_with_valid_id_but_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_for_rent_detail', kwargs={'id': pytest.house_id}))
        assert response.status_code == 404

    def test_rent_house_with_valid_id(self, authenticated_client, create_house_rent):
        response = authenticated_client.get(reverse('available_for_rent_detail', kwargs={'id': pytest.house_id}))
        assert response.status_code == 200

    def test_rent_house_with_invalid_id(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_for_rent_detail', kwargs={'id': 10}))
        assert response.status_code == 404

    def test_rent_house_list(self, authenticated_client, create_house_rent):
        response = authenticated_client.get(reverse('available_for_rent') + "?filter_city=ahmedabad")
        assert response.status_code == 200