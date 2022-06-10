from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


def validate_username(username):
    """
    Function to validate the username
    :param username: takes in username and validates it
    :return: validated username
    """
    if len(username) < 3:
        raise ValidationError("Username too short.Please enter a username of atleast 3 characters.")
    elif len(username) > 30:
        raise ValidationError("Username too long.Please enter a username of not greater than 30 characters.")
    elif not username.islower():
        raise ValidationError("Username should consists of lower case alphabets only.")
    elif " " in username:
        raise ValidationError("Username cannot contain spaces.")
    else:
        return True


def validate_name(name):
    """
    Function to validate the first name and last name of the user
    :param name: takes in the first name or last name and validates it
    :return: validated name
    """
    if " " in name:
        raise ValidationError(f"{name} cannot contain spaces.")
    elif name.isalpha():
        return name
    else:
        raise ValidationError(f"{name} is invalid. Enter a valid name")


# Custom User Manager

class UserManager(BaseUserManager):
    def create_user(self, **kwargs):  # fname, lname, username, email, phone_number, address, profile_image, password=None, password2=None):
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

    def create_superuser(self, email, fname, lname, username, phone_number, address, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email,
            fname=fname,
            lname=lname,
            username=username,
            phone_number=phone_number,
            address=address,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




# Custom User Model

class User(AbstractBaseUser):
    fname = models.CharField(max_length=200, verbose_name='First Name', validators=[validate_name])
    lname = models.CharField(max_length=200, verbose_name='Last Name', validators=[validate_name])
    username = models.CharField(max_length=255, unique=True, verbose_name='Username', validators=[validate_username])
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    phone_number = PhoneNumberField(unique=True)
    address = models.TextField(verbose_name='Address')
    profile_image = models.ImageField(default = 'default.jpg', upload_to='uploads/', null=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'username', 'phone_number', 'address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
