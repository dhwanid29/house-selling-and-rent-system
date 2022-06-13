import re
from rest_framework.exceptions import ValidationError

from constants import password_validation_error, username_short_error, username_long_error, only_lowercase, \
    no_spaces_allowed, invalid_name, name_no_spaces_allowed


def validate_password(password):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!#%*?&]{8,20}$"

    if re.fullmatch(reg, password):
        return password
    else:
        raise ValidationError(password_validation_error)


def validate_username(username):
    """
    Function to validate the username
    :param username: takes in username and validates it
    :return: validated username
    """
    if len(username) < 3:
        raise ValidationError(username_short_error)
    elif len(username) > 30:
        raise ValidationError(username_long_error)
    elif not username.islower():
        raise ValidationError(only_lowercase)
    elif " " in username:
        raise ValidationError(no_spaces_allowed)
    else:
        return True


def validate_name(name):
    """
    Function to validate the first name and last name of the user
    :param name: takes in the first name or last name and validates it
    :return: validated name
    """
    if " " in name:
        raise ValidationError(name_no_spaces_allowed)
    elif name.isalpha():
        return name
    else:
        raise ValidationError(invalid_name)