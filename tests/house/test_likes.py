import pytest
from django.urls import reverse
from house.models import Likes, LikesUser


@pytest.mark.django_db(True)
class TestAddHouseLike:
    def test_add_house_like_valid_data(self, authenticated_client, create_house, create_house_like):
        house_like_data = {
            "house": pytest.house_id
        }
        check_house = Likes.objects.filter(house=house_like_data['house']).first()
        if check_house:
            check_like = LikesUser.objects.filter(likes=check_house.id, user=pytest.user_id)

            if check_like:
                response = authenticated_client.post(reverse('likes-list'), house_like_data)
                assert response.status_code == 400
            else:
                response = authenticated_client.post(reverse('likes-list'), house_like_data)
                assert response.status_code == 201
        else:
            response = authenticated_client.post(reverse('likes-list'), house_like_data)
            assert response.status_code == 201

    def test_add_house_like_no_data(self, authenticated_client, create_house, create_house_like):
        response = authenticated_client.post(reverse('likes-list'), )
        assert response.status_code == 404

    def test_add_house_like_wrong_house_id(self, authenticated_client, create_house, create_house_like):
        house_like_data = {
            "house": 10,
        }
        response = authenticated_client.post(reverse('likes-list'), house_like_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestGetHouseLike:
    def test_retrieve_house_like_with_valid_id(self, authenticated_client, create_house, create_house_like):
        response = authenticated_client.get(reverse('likes-detail', kwargs={'house': pytest.house_id}))
        assert response.status_code == 200

    def test_retrieve_house_like_with_invalid_id(self, authenticated_client, create_house, create_house_like):
        response = authenticated_client.get(reverse('likes-detail', kwargs={'house': 10}))
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestUpdateHouseLike:
    def test_update_house_like_with_valid_id(self, authenticated_client, create_house, create_house_like):
        house_like_data = {
            "house": pytest.house_id,
        }
        response = authenticated_client.put(reverse('likes-detail', kwargs={'house': pytest.house_id}),
                                                house_like_data)
        assert response.status_code == 200

    def test_update_house_like_with_invalid_id(self, authenticated_client, create_house, create_house_like):
        house_like_data = {
            "house": 10,
        }
        response = authenticated_client.put(reverse('likes-detail', kwargs={'house': pytest.house_id}),
                                            house_like_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestDeleteHouseLike:
    def test_delete_house_like_with_valid_house_id(self, authenticated_client, create_house, create_house_like):
        response = authenticated_client.delete(reverse('likes-detail', kwargs={'house': pytest.house_id}))
        assert response.status_code == 204

    def test_delete_house_like_with_invalid_house_id(self, authenticated_client, create_house, create_house_like):
        response = authenticated_client.delete(reverse('likes-detail', kwargs={'house': 10}))
        assert response.status_code == 404