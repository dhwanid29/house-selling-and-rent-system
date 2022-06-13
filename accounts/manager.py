from django.contrib.auth.models import BaseUserManager
from constants import email_required

# Custom User Manager


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not kwargs.get('email'):
            raise ValueError(email_required)

        kwargs.pop('password2', None)
        user = self.model(**kwargs)

        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, phone_number, address, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            address=address,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
