import pytest
from django.urls import reverse
from house.models import Favourites, FavouritesUser


@pytest.mark.django_db(True)
class TestAddHouseFavourites:
    def test_add_house_favourite_valid_data(self, authenticated_client, create_house, create_house_favourites):
        house_favourite_data = {
            "house": pytest.house_id
        }
        check_house = Favourites.objects.filter(house=house_favourite_data['house']).first()
        if check_house:
            check_favourite = FavouritesUser.objects.filter(favourites=check_house.id, user=pytest.user_id)

            if check_favourite:
                response = authenticated_client.post(reverse('favourites-list'), house_favourite_data)
                assert response.status_code == 400
            else:
                response = authenticated_client.post(reverse('favourites-list'), house_favourite_data)
                assert response.status_code == 201
        else:
            response = authenticated_client.post(reverse('favourites-list'), house_favourite_data)
            assert response.status_code == 201

    def test_add_house_favourite_no_data(self, authenticated_client, create_house, create_house_favourites):
        response = authenticated_client.post(reverse('favourites-list'), )
        assert response.status_code == 404

    def test_add_house_favourite_wrong_house_id(self, authenticated_client, create_house, create_house_favourites):
        house_favourite_data = {
            "house": 10,
        }
        response = authenticated_client.post(reverse('favourites-list'), house_favourite_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestGetHouseFavourite:
    def test_retrieve_house_favourite_with_valid_id(self, authenticated_client, create_house, create_house_favourites):
        response = authenticated_client.get(reverse('favourites-detail', kwargs={'house': pytest.house_id}))
        assert response.status_code == 200

    def test_retrieve_house_favourite_with_invalid_id(self, authenticated_client, create_house, create_house_favourites):
        response = authenticated_client.get(reverse('favourites-detail', kwargs={'house': 10}))
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestUpdateHouseFavourite:
    def test_update_house_favourite_with_valid_id(self, authenticated_client, create_house, create_house_favourites):
        house_favourite_data = {
            "house": pytest.house_id,
        }
        response = authenticated_client.put(reverse('favourites-detail', kwargs={'house': pytest.house_id}),
                                                house_favourite_data)
        assert response.status_code == 200

    def test_update_house_favourite_with_invalid_id(self, authenticated_client, create_house, create_house_favourites):
        house_favourite_data = {
            "house": 10,
        }
        response = authenticated_client.put(reverse('favourites-detail', kwargs={'house': pytest.house_id}),
                                            house_favourite_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestDeleteHouseFavourites:
    def test_delete_house_favourite_with_valid_house_id(self, authenticated_client, create_house,
                                                        create_house_favourites):
        response = authenticated_client.delete(reverse('favourites-detail', kwargs={'house': pytest.house_id}))
        assert response.status_code == 204

    def test_delete_house_favourite_with_invalid_house_id(self, authenticated_client, create_house,
                                                          create_house_favourites):
        response = authenticated_client.delete(reverse('favourites-detail', kwargs={'house': 10}))
        assert response.status_code == 404