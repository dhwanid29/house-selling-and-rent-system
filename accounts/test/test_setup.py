from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'first_name': "abcd",
            'last_name': "abcd",
            'email': "email@gmail.com",
            'username': "abcd",
            'phone_number': "+91 8566783456",
            'address': "gota",
            'password': "Abcd@1234",
            'password2': "Abcd@1234",
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
