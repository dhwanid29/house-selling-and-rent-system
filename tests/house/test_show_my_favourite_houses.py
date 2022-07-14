import pytest
from django.urls import reverse


@pytest.mark.django_db(True)
class TestMyFavouriteHouse:
    def test_my_favourite_houses_with_valid_id(self, authenticated_client, create_house_favourites):
        response = authenticated_client.get(reverse('my_favourites', kwargs={'user': pytest.user_id}))
        print(response.data, 'sdhj')
        assert response.status_code == 200

