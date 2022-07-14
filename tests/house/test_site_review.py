import pytest
from django.urls import reverse
from house.models import SiteReview


@pytest.mark.django_db(True)
class TestAddSiteReview:
    def test_add_site_review_valid_data(self, authenticated_client, create_site_review):
        site_review_data = {
            "review": "good"
        }
        check_site_review = SiteReview.objects.filter(user=pytest.user_id)
        if check_site_review:
            response = authenticated_client.post(reverse('site_review-list'), site_review_data)
            assert response.status_code == 400
        else:
            response = authenticated_client.post(reverse('site_review-list'), site_review_data)
            assert response.status_code == 201

    def test_add_site_review_no_data(self, authenticated_client, create_site_review):
        response = authenticated_client.post(reverse('site_review-list'))
        assert response.status_code == 400

    def test_add_site_review_empty_review(self, authenticated_client, create_site_review):
        site_review_data = {
            "review": ""
        }
        response = authenticated_client.post(reverse('site_review-list'), site_review_data)
        assert response.status_code == 400


@pytest.mark.django_db(True)
class TestGetSiteReview:
    def test_retrieve_site_review_with_valid_id(self, authenticated_client, create_site_review):
        response = authenticated_client.get(reverse('site_review-detail', kwargs={'user': pytest.user_id}))
        assert response.status_code == 200

    def test_retrieve_site_review_with_invalid_id(self, authenticated_client, create_site_review):
        response = authenticated_client.get(reverse('site_review-detail', kwargs={'user': 10}))
        assert response.status_code == 404

    def test_site_review_list(self, authenticated_client, create_site_review):
        response = authenticated_client.get(reverse('site_review-list'))
        assert response.status_code == 200


@pytest.mark.django_db(True)
class TestUpdateHouseReview:
    def test_update_site_review_with_valid_data(self, authenticated_client, create_site_review):
        site_review_data = {
            "house": pytest.house_id,
            "review": "good"
        }
        response = authenticated_client.put(reverse('site_review-detail', kwargs={'user': pytest.user_id}),
                                            site_review_data)
        assert response.status_code == 200


@pytest.mark.django_db(True)
class TestDeleteHouseReview:
    def test_delete_site_review_with_valid_site_review_id(self, authenticated_client, create_site_review):
        response = authenticated_client.delete(reverse('site_review-detail', kwargs={'user': pytest.user_id}))
        assert response.status_code == 204

    def test_delete_site_review_with_invalid_site_review_id(self, authenticated_client, create_site_review):
        response = authenticated_client.delete(reverse('site_review-detail', kwargs={'user': 10}))
        assert response.status_code == 404