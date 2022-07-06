import pytest
from accounts.models import User


@pytest.fixture
def user():
    # user_data = {
    #     "first_name": "dhwani",
    #     "last_name": "dadhich",
    #     "username": "dhwani",
    #     "email": "dhwani@gmail.com",
    #     "phone_number": "+918670777787",
    #     "address": "gota",
    #     "password": "Abcd@1234",
    #     "password2": "Abcd@1234"
    # }
    user = User.objects.create(first_name="dhwani", last_name="dadhich", username="dhwani", email="dhwani@gmail.com",
                               phone_number="+918670777787", address="gota")
    user.set_password(raw_password='Abcd@1234')
    user.save()
    return user
