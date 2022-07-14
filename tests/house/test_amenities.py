import pytest
from django.urls import reverse
from house.models import Preference


@pytest.mark.django_db(True)
class TestAddHouseAmenities:
    def test_add_house_amenities_valid_data(self, authenticated_client, create_house_amenities):
        house_amenities_data = {
            "name": "Garden"
        }
        check_house_amenities = Preference.objects.filter(user=pytest.user_id)
        if check_house_amenities:
            response = authenticated_client.post(reverse('add_amenities'), house_amenities_data)
            assert response.status_code == 400
        else:
            response = authenticated_client.post(reverse('add_amenities'), house_amenities_data)
            assert response.status_code == 201

    def test_add_house_amenities_no_data(self, authenticated_client, create_house_amenities):
        response = authenticated_client.post(reverse('add_amenities'))
        assert response.status_code == 400


@pytest.mark.django_db(True)
class TestGetHouseAmenities:
    def test_retrieve_house_amenities_list(self, authenticated_client, create_house_amenities):
        response = authenticated_client.get(reverse('view_amenities'))
        assert response.status_code == 200


@pytest.mark.django_db(True)
class TestUpdateHouseAmenities:
    def test_update_house_amenities_with_valid_id(self, authenticated_client, create_house_amenities):
        house_amenities_data = {
            "name": "Garden"
        }
        response = authenticated_client.put(reverse('amenities_update', kwargs={'id': pytest.amenities}),
                                            house_amenities_data)
        assert response.status_code == 200

    def test_update_house_amenities_with_invalid_id(self, authenticated_client, create_house_amenities):
        house_amenities_data = {
            "name": "Garden"
        }
        response = authenticated_client.put(reverse('amenities_update', kwargs={'id': 15}), house_amenities_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestDeleteHouseAmenities:
    def test_delete_house_amenities_with_valid_id(self, authenticated_client, create_house_amenities):
        response = authenticated_client.delete(reverse('amenities_update', kwargs={'id': pytest.amenities}))
        assert response.status_code == 204

    def test_delete_house_amenities_with_invalid_id(self, authenticated_client, create_house_amenities):
        response = authenticated_client.delete(reverse('amenities_update', kwargs={'id': 10}))
        assert response.status_code == 404