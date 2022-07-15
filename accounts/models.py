from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from accounts.manager import UserManager
from accounts.validations import validate_name, validate_username


# Custom User Model


class User(AbstractBaseUser):
    """
    User Model
    """
    first_name = models.CharField(max_length=200, verbose_name='First Name', validators=[validate_name])
    last_name = models.CharField(max_length=200, verbose_name='Last Name', validators=[validate_name])
    username = models.CharField(max_length=255, unique=True, verbose_name='Username', validators=[validate_username])
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    phone_number = PhoneNumberField(unique=True)
    address = models.TextField(verbose_name='Address')
    profile_image = models.ImageField(default = 'default.jpg', upload_to='profile_images/')
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_number', 'address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
