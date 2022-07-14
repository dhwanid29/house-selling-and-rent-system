import pytest
from django.urls import reverse
from house.models import Preference


@pytest.mark.django_db(True)
class TestAddHousePreference:
    def test_add_house_preference_valid_data(self, authenticated_client, create_house, create_preference):
        house_preference_data = {
            "residence_name": "shayona green",
            "no_of_bedrooms": "2",
            "state": "gujarat",
            "city": "ahmedabad",
            "selling_choice": "Sell"
        }
        check_house_preference = Preference.objects.filter(user=pytest.user_id)
        if check_house_preference:
            response = authenticated_client.post(reverse('preferences-list'), house_preference_data)
            assert response.status_code == 400
        else:
            response = authenticated_client.post(reverse('preferences-list'), house_preference_data)
            assert response.status_code == 201

    def test_add_house_preference_no_data(self, authenticated_client, create_house, create_preference):
        response = authenticated_client.post(reverse('preferences-list'))
        assert response.status_code == 400

    def test_add_house_preference_no_residence_name(self, authenticated_client, create_house, create_preference):
        house_preference_data = {
            "no_of_bedrooms": "2",
            "state": "gujarat",
            "city": "ahmedabad",
            "selling_choice": "Sell"
        }
        response = authenticated_client.post(reverse('preferences-list'), house_preference_data)
        assert response.status_code == 400

    def test_add_house_preference_no_no_of_bedrooms(self, authenticated_client, create_house, create_preference):
        house_preference_data = {
            "residence_name": "shayona green",
            "state": "gujarat",
            "city": "ahmedabad",
            "selling_choice": "Sell"
        }
        response = authenticated_client.post(reverse('preferences-list'), house_preference_data)
        assert response.status_code == 400

    def test_add_house_preference_no_state(self, authenticated_client, create_house, create_preference):
        house_preference_data = {
            "residence_name": "shayona green",
            "no_of_bedrooms": "2",
            "city": "ahmedabad",
            "selling_choice": "Sell"
        }
        response = authenticated_client.post(reverse('preferences-list'), house_preference_data)
        assert response.status_code == 400

    def test_add_house_preference_no_city(self, authenticated_client, create_house, create_preference):
        house_preference_data = {
            "residence_name": "shayona green",
            "no_of_bedrooms": "2",
            "state": "gujarat",
            "selling_choice": "Sell"
        }
        response = authenticated_client.post(reverse('preferences-list'), house_preference_data)
        assert response.status_code == 400


@pytest.mark.django_db(True)
class TestGetHousePreference:
    def test_retrieve_house_preference_with_valid_id(self, authenticated_client, create_house, create_preference):
        response = authenticated_client.get(reverse('preferences-detail', kwargs={'user': pytest.user_id}))
        assert response.status_code == 200

    def test_retrieve_house_preference_with_invalid_id(self, authenticated_client, create_house, create_preference):
        response = authenticated_client.get(reverse('preferences-detail', kwargs={'user': 10}))
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestUpdateHousePreference:
    def test_update_house_preference_with_valid_id(self, authenticated_client, create_house, create_preference):
        house_preference_data = {
            "residence_name": "shayona green",
            "no_of_bedrooms": "2",
            "state": "gujarat",
            "selling_choice": "Sell"
        }
        response = authenticated_client.put(reverse('preferences-detail', kwargs={'user': pytest.user_id}),
                                            house_preference_data)
        assert response.status_code == 200

    def test_update_house_preference_with_invalid_id(self, authenticated_client, create_house, create_preference):
        house_preference_data = {
            "residence_name": "shayona green",
            "no_of_bedrooms": "2",
            "state": "gujarat",
            "selling_choice": "Sell"
        }
        response = authenticated_client.put(reverse('preferences-detail', kwargs={'user': 15}), house_preference_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestDeleteHousePreference:
    def test_delete_house_preference_with_valid_house_id(self, authenticated_client, create_house, create_preference):
        response = authenticated_client.delete(reverse('preferences-detail', kwargs={'user': pytest.user_id}))
        assert response.status_code == 204

    def test_delete_house_preference_with_invalid_house_id(self, authenticated_client, create_house):
        response = authenticated_client.delete(reverse('preferences-detail', kwargs={'user': 10}))
        assert response.status_code == 404