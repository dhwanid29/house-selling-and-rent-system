import pytest
from django.urls import reverse
from house.models import HouseReview


@pytest.mark.django_db(True)
class TestAddHouseReview:
    def test_add_house_review_valid_data(self, authenticated_client, create_house_review, create_house):
        house_review_data = {
            "house": pytest.house_id,
            "review": "good"
        }
        check_house_review = HouseReview.objects.filter(house=house_review_data['house'], user=pytest.user_id)
        if check_house_review:
            response = authenticated_client.post(reverse('house_review-list'), house_review_data)
            assert response.status_code == 400
        else:
            response = authenticated_client.post(reverse('house_review-list'), house_review_data)
            assert response.status_code == 201

    def test_add_house_review_no_data(self, authenticated_client, create_house_review, create_house):
        response = authenticated_client.post(reverse('house_review-list'), )
        assert response.status_code == 404

    def test_add_house_review_no_house(self, authenticated_client, create_house_review, create_house):
        house_review_data = {
            "review": "good"
        }
        response = authenticated_client.post(reverse('house_review-list'), house_review_data)
        assert response.status_code == 404

    def test_add_house_review_no_review(self, authenticated_client, create_house_review, create_house):
        house_review_data = {
            "house": pytest.house_id,
        }
        response = authenticated_client.post(reverse('house_review-list'), house_review_data)
        assert response.status_code == 400

    def test_add_house_review_wrong_house_id(self, authenticated_client, create_house_review, create_house):
        house_review_data = {
            "house": 10,
        }
        response = authenticated_client.post(reverse('house_review-list'), house_review_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestGetHouseReview:
    def test_retrieve_house_review_with_valid_id(self, authenticated_client, create_house_review, create_house):
        response = authenticated_client.get(reverse('house_review-detail', kwargs={'id': pytest.house_review_id}))
        assert response.status_code == 200

    def test_retrieve_house_review_with_invalid_id(self, authenticated_client, create_house_review, create_house):
        response = authenticated_client.get(reverse('house_review-detail', kwargs={'id': 10}))
        assert response.status_code == 404

    def test_house_review_list(self, authenticated_client, create_house_review, create_house):
        response = authenticated_client.get(reverse('house_review-list'))
        assert response.status_code == 200


@pytest.mark.django_db(True)
class TestUpdateHouseReview:
    def test_update_house_review_with_valid_id(self, authenticated_client, create_house_review, create_house):
        house_review_data = {
            "house": pytest.house_id,
            "review": "good"
        }
        response = authenticated_client.put(reverse('house_review-detail', kwargs={'id': pytest.house_review_id}),
                                                house_review_data)
        assert response.status_code == 200

    def test_update_house_review_with_invalid_id(self, authenticated_client, create_house_review, create_house):
        house_review_data = {
            "house": 10,
            "review": "good"
        }
        response = authenticated_client.put(reverse('house_review-detail', kwargs={'id': pytest.house_review_id}),
                                            house_review_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestDeleteHouseReview:
    def test_delete_house_review_with_valid_house_review_id(self, authenticated_client, create_house_review,
                                                            create_house):
        response = authenticated_client.delete(reverse('house_review-detail', kwargs={'id': pytest.house_review_id}))
        assert response.status_code == 204

    def test_delete_house_review_with_invalid_house_review_id(self, authenticated_client, create_house_review,
                                                              create_house):
        response = authenticated_client.delete(reverse('house_review-detail', kwargs={'id': 10}))
        assert response.status_code == 404