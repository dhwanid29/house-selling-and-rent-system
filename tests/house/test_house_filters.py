import pytest
from django.urls import reverse


@pytest.mark.django_db(True)
class TestAvailableHousesFilter:

    def test_rent_house_list_filter_city(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_city=ahmedabad")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['city'] == 'ahmedabad'
        assert response.status_code == 200

    def test_rent_house_list_filter_city_no_data_fetched(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_city=hello")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_filter_state(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_state=gujarat")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['state'] == 'gujarat'
        assert response.status_code == 200

    def test_rent_house_list_filter_state_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_state=hello")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_price_min(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?price_min=20000")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['price'] == '20000.00'
        assert response.status_code == 200

    def test_rent_house_list_price_min_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?price_min=20000000")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_price_min_invalid_price(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?price_min=hello")
        assert response.status_code == 400

    def test_rent_house_list_price_max(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?price_max=20000")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['price'] == '20000.00'
        assert response.status_code == 200

    def test_rent_house_list_price_max_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?price_min=2000000000")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_price_max_invalid_price(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?price_min=hello")
        assert response.status_code == 400

    def test_rent_house_list_filter_amenities(self, authenticated_client, create_house, create_house_amenities):
        response = authenticated_client.get(reverse('available_houses_filter') + f"?filter_amenities={pytest.amenities}")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['amenities'] == [pytest.amenities]
        assert response.status_code == 200

    def test_rent_house_list_filter_amenities_no_data(self, authenticated_client, create_house, create_house_amenities):
        response = authenticated_client.get(reverse('available_houses_filter') + f"?filter_amenities=10")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_filter_no_of_bedrooms(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_no_of_bedrooms=3")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['no_of_bedrooms'] == 3
        assert response.status_code == 200

    def test_rent_house_list_filter_no_of_bedrooms_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_no_of_bedrooms=5")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_filter_possession(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_possession=Within 6 months")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['possession'] == 'Within 6 months'
        assert response.status_code == 200

    def test_rent_house_list_filter_possession_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_possession=hello")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_filter_project_status(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_project_status=Constructed")
        assert len(response.data['data']) != 0
        get_data = response.data['data']
        for i in get_data:
            assert i['project_status'] == 'Constructed'
        assert response.status_code == 200

    def test_rent_house_list_filter_project_status_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?filter_project_status=hello")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_date_before(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?date_before=2022-07-15")
        assert len(response.data['data']) != 0
        assert response.status_code == 200

    def test_rent_house_list_date_before_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?date_before=2022-07-10")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_date_before_invalid_date(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?date_before=hello")
        assert response.status_code == 400

    def test_rent_house_list_date_after(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?date_after=2022-07-13")
        assert len(response.data['data']) != 0
        assert response.status_code == 200

    def test_rent_house_list_date_after_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?date_after=2022-07-19")
        assert len(response.data['data']) == 0
        assert response.status_code == 200

    def test_rent_house_list_date_after_invalid_date(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?date_after=2022-07-19")
        assert response.status_code == 200

    def test_rent_house_list_sort_by_price_asc(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?sort_by_price_asc=price")
        assert len(response.data['data']) != 0
        assert response.status_code == 200

    def test_rent_house_list_sort_by_price_desc(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?sort_by_price_desc=price")
        assert len(response.data['data']) != 0
        assert response.status_code == 200

    def test_rent_house_list_search(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?search=shayona")
        assert response.status_code == 200

    def test_rent_house_list_search_no_data(self, authenticated_client, create_house):
        response = authenticated_client.get(reverse('available_houses_filter') + "?search=nonsense")
        assert response.status_code == 200