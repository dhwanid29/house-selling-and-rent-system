from django.contrib.auth.models import BaseUserManager

# Custom User Manager

class UserManager(BaseUserManager):
    def create_user(self, **kwargs):  # first_name, last_name, username, email, phone_number, address, profile_image, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not kwargs.get('email'):
            raise ValueError('Users must have an email address')

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
