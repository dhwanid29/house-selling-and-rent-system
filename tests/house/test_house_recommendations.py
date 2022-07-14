import pytest
from django.urls import reverse


@pytest.mark.django_db(True)
class TestRecommendedHouses:
    def test_recommended_house_with_valid_id(self, authenticated_client, create_preference):
        response = authenticated_client.get(reverse('recommended_houses', kwargs={'user': pytest.user_id}))
        assert response.status_code == 200
