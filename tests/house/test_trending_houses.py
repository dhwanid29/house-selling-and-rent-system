import pytest
from django.urls import reverse


@pytest.mark.django_db(True)
class TestTrendingHouses:
    def test_trending_house_list(self, authenticated_client):
        response = authenticated_client.get(reverse('trending_houses'))
        assert response.status_code == 200