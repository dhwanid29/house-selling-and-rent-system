import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


@pytest.mark.django_db(True)
class TestAddHouseImages:
    def test_add_house_image_valid_data(self, authenticated_client, create_house, create_house_images):
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')
        house_image_data = {
            "house": pytest.house_id,
            "house_image": image
        }
        response = authenticated_client.post(reverse('house_images-list'), house_image_data)
        assert response.status_code == 201

    def test_add_house_image_no_data(self, authenticated_client, create_house, create_house_images):
        response = authenticated_client.post(reverse('house_images-list'))
        assert response.status_code == 404

    def test_add_house_image_no_house(self, authenticated_client, create_house, create_house_images):
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')
        house_image_data = {
            "house_image": image
        }
        response = authenticated_client.post(reverse('house_images-list'), house_image_data)
        assert response.status_code == 404

    def test_add_house_image_no_house_image(self, authenticated_client, create_house, create_house_images):
        house_image_data = {
            "house": pytest.house_id
        }
        response = authenticated_client.post(reverse('house_images-list'), house_image_data)
        assert response.status_code == 400

    def test_add_house_image_invalid_house_image(self, authenticated_client, create_house, create_house_images):
        house_image_data = {
            "house": pytest.house_id,
            "house_image": "abc.png"
        }
        response = authenticated_client.post(reverse('house_images-list'), house_image_data)
        assert response.status_code == 400

    def test_add_house_image_invalid_house_id(self, authenticated_client, create_house, create_house_images):
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')
        house_image_data = {
            "house": 10,
            "house_image": image
        }
        response = authenticated_client.post(reverse('house_images-list'), house_image_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestGetHouseImages:
    def test_retrieve_house_image_with_valid_id(self, authenticated_client, create_house, create_house_images):
        response = authenticated_client.get(reverse('house_images-detail', kwargs={'id': pytest.house_image_id}))
        assert response.status_code == 200

    def test_retrieve_house_image_with_invalid_id(self, authenticated_client, create_house, create_house_images):
        response = authenticated_client.get(reverse('house_images-detail', kwargs={'id': 100}))
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestUpdateHousePreference:
    def test_update_house_image_with_valid_id(self, authenticated_client, create_house, create_house_images):
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image1.jpg', image_data.read(), content_type='multipart/form-data')
        house_image_data = {
            "house": pytest.house_id,
            "house_image": image
        }
        response = authenticated_client.put(reverse('house_images-detail', kwargs={'id': pytest.house_image_id}),
                                            house_image_data)
        assert response.status_code == 200

    def test_update_house_image_with_invalid_id(self, authenticated_client, create_house, create_house_images):
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')
        house_image_data = {
            "house": pytest.house_id,
            "house_image": image
        }
        response = authenticated_client.put(reverse('house_images-detail', kwargs={'id': 15}), house_image_data)
        assert response.status_code == 404


@pytest.mark.django_db(True)
class TestDeleteHouseImages:
    def test_delete_house_image_with_valid_house_id(self, authenticated_client, create_house, create_house_images):
        response = authenticated_client.delete(reverse('house_images-detail', kwargs={'id': pytest.house_image_id}))
        assert response.status_code == 204

    def test_delete_house_image_with_invalid_house_id(self, authenticated_client, create_house):
        response = authenticated_client.delete(reverse('house_images-detail', kwargs={'id': 10}))
        assert response.status_code == 404