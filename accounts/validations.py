import re
from rest_framework.exceptions import ValidationError

from constants import PASSWORD_VALIDATION_ERROR, USERNAME_SHORT_ERROR, USERNAME_LONG_ERROR, ONLY_LOWERCASE, \
    NO_SPACES_ALLOWED, INVALID_NAME, NAME_NO_SPACES_ALLOWED


def validate_password(password):
    """
    Function to validate user password
    :param password: takes in password and validates it
    :return: validated password
    """
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!#%*?&]{8,20}$"

    if re.fullmatch(reg, password):
        return password
    else:
        raise ValidationError(PASSWORD_VALIDATION_ERROR)


def validate_username(username):
    """
    Function to validate the username
    :param username: takes in username and validates it
    :return: validated username
    """
    if len(username) < 3:
        raise ValidationError(USERNAME_SHORT_ERROR)
    elif len(username) > 30:
        raise ValidationError(USERNAME_LONG_ERROR)
    elif not username.islower():
        raise ValidationError(ONLY_LOWERCASE)
    elif " " in username:
        raise ValidationError(NO_SPACES_ALLOWED)
    else:
        return True


def validate_name(name):
    """
    Function to validate the first name and last name of the user
    :param name: takes in the first name or last name and validates it
    :return: validated name
    """
    if " " in name:
        raise ValidationError(NAME_NO_SPACES_ALLOWED)
    elif name.isalpha():
        return name
    else:
        raise ValidationError(INVALID_NAME)