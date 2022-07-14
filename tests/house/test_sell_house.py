import pytest
from django.urls import reverse


@pytest.mark.django_db(True)
class TestAddHouse:
    def test_add_house_valid_data(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 201

    def test_add_house_no_data(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "",
            "price": "",
            "no_of_bedrooms": "",
            "no_of_lift": "",
            "no_of_floors": "",
            "no_of_building": "",
            "state": "",
            "city": "",
            "sqft": "",
            "amenities": [],
            "possession": "",
            "selling_choice": "",
            "address": "",
            "project_status": ""
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_amenities(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_residence_name(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_price(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_number_of_bedrooms(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_number_of_lift(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_number_of_floors(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_number_of_building(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_state(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_city(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400

    def test_add_house_no_sqft(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "ahmedabad",
            "city": "ahmedabad",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.post(reverse('house_detail-list'), house_data)
        assert response.status_code == 400


@pytest.mark.django_db(True)
class TestGetHouse:
    def test_retrieve_house_with_valid_id(self, authenticated_client, create_house_amenities, create_house):
        response = authenticated_client.get(reverse('house_detail-detail', kwargs={'id': pytest.house_id}))
        assert response.status_code == 200

    def test_retrieve_house_with_invalid_id(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('house_detail-detail', kwargs={'id': 10}))
        assert response.status_code == 404

    def test_house_list(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('house_detail-list'))
        assert response.status_code == 200


@pytest.mark.django_db(True)
class TestUpdateHouse:
    def test_update_house_with_valid_id(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "guj",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.put(reverse('house_detail-detail', kwargs={'id': pytest.house_id}), house_data)
        assert response.status_code == 200

    def test_update_house_with_invalid_id(self, authenticated_client, create_house_amenities, create_house):
        house_data = {
            "residence_name": "shayona green",
            "price": "22498",
            "no_of_bedrooms": "3",
            "no_of_lift": "2",
            "no_of_floors": "5",
            "no_of_building": "13",
            "state": "guj",
            "city": "ahmedabad",
            "sqft": "1500",
            "amenities": [pytest.amenities],
            "possession": "Within 6 months",
            "selling_choice": "Rent",
            "address": "gota",
            "project_status": "Constructed"
        }
        response = authenticated_client.put(reverse('house_detail-detail', kwargs={'id': 10}), house_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestDeleteHouse:
    def test_delete_house_with_valid_house_id(self, authenticated_client, create_house_amenities, create_house):
        response = authenticated_client.delete(reverse('house_detail-detail', kwargs={'id': pytest.house_id}))
        assert response.status_code == 204

    def test_delete_house_with_invalid_house_id(self, authenticated_client, create_house_amenities, create_house):
        response = authenticated_client.delete(reverse('house_detail-detail', kwargs={'id': 10}))
        assert response.status_code == 404