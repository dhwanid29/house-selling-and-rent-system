import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


@pytest.mark.django_db(True)
class TestUserProfileView:

    def test_view_user_profile(self, authenticated_client):
        response = authenticated_client.get(reverse('profile'))
        assert response.status_code == 200


@pytest.mark.django_db(True)
class TestUserProfileUpdate:

    def test_update_user_profile(self, authenticated_client):
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')
        update_profile_data = {
            "first_name": "dhwanid",
            "last_name": "dadhichhh",
            "username": "dhwani",
            "email": "dhwan@gmail.com",
            "address": "gota",
            "profile_image": image
        }
        response = authenticated_client.put(reverse('profile'), update_profile_data, format="multipart")
        assert  response.status_code == 200


        # get_users = User.objects.all()
        # print(get_users, "hahah")
        # check_email = User.objects.filter(email=update_profile_data["email"]).first()
        # print(check_email, "uooo")
        # if check_email:
        #     response = authenticated_client.put(reverse('profile'), update_profile_data, format="multipart")
        #     print(response.data, "hey")
        #     assert response.status_code == 400
        # else:
        #     response = authenticated_client.put(reverse('profile'), update_profile_data, format="multipart")
        #     print(response.data, "uiuiu")
        #     assert  response.status_code == 200

    def test_update_user_profile_with_wrong_email_format(self, authenticated_client, create_user):
        image_data = File(open('media/default.jpg', 'rb'))
        image = SimpleUploadedFile('image.jpg', image_data.read(), content_type='multipart/form-data')
        update_profile_data = {
            "first_name": "dhwanid",
            "last_name": "dadhichhh",
            "email": "dadhichdhwani29gmail.com",
            "address": "gota",
            "profile_image": image
        }
        response = authenticated_client.put(reverse('profile'), update_profile_data, format="multipart")
        assert  response.status_code == 400

    def test_update_user_profile_with_wrong_file_format(self, authenticated_client, create_user):
        update_profile_data = {
            "first_name": "dhwanid",
            "last_name": "dadhichhh",
            "email": "dhwani@gmail.com",
            "address": "gota",
            "profile_image": "image"
        }
        response = authenticated_client.put(reverse('profile'), update_profile_data, format="multipart")
        assert  response.status_code == 400


@pytest.mark.django_db(True)
class TestUserProfileDelete:

    def test_delete_user_profile(self, authenticated_client):
        response = authenticated_client.delete(reverse('profile'))
        assert  response.status_code == 204


@pytest.mark.django_db(True)
class TestUserProfileEmailUpdateLink:

    def test_update_email_link_valid_data(self, authenticated_client, user_token):
        email_update_data = {
            "email": "dhwani@gmail.com",
            "password": "Abcd@1234"
        }
        response = authenticated_client.post(reverse('email_update', kwargs={'uid': pytest.uid, 'token': pytest.token}),
                                             email_update_data)
        assert  response.status_code == 200

    def test_update_email_link_with_wrong_email(self, authenticated_client, user_token):
        email_update_data = {
            "email": "dhwansi@gmail.com",
            "password": "Abcd@1234"
        }
        response = authenticated_client.post(reverse('email_update', kwargs={'uid': pytest.uid, 'token': pytest.token}),
                                             email_update_data)
        assert  response.status_code == 404

    def test_update_email_link_with_wrong_password(self, authenticated_client, user_token):
        email_update_data = {
            "email": "dhwani@gmail.com",
            "password": "Abcd@12345"
        }
        response = authenticated_client.post(reverse('email_update', kwargs={'uid': pytest.uid, 'token': pytest.token}),
                                             email_update_data)
        assert  response.status_code == 404

    def test_update_email_link_with_no_data(self, authenticated_client, user_token):
        response = authenticated_client.post(reverse('email_update', kwargs={'uid': pytest.uid, 'token':  pytest.token}))
        assert  response.status_code == 404