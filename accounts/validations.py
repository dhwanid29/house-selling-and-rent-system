import datetime
import re
from rest_framework.exceptions import ValidationError

from constants import PASSWORD_VALIDATION_ERROR, USERNAME_SHORT_ERROR, USERNAME_LONG_ERROR, ONLY_LOWERCASE, \
    NO_SPACES_ALLOWED, INVALID_NAME, NAME_NO_SPACES_ALLOWED, PASSWORD_SHORT_LENGTH_ERROR, PASSWORD_LONG_LENGTH_ERROR, \
    PASSWORD_CONTAINS_NO_DIGIT_ERROR, PASSWORD_CONTAINS_NO_UPPERCASE_ERROR, PASSWORD_CONTAINS_NO_LOWERCASE_ERROR, \
    PASSWORD_CONTAINS_NO_SPECIAL_CHARACTER_ERROR, DATE_ERROR, PRICE_ERROR


def validate_password(password):
    """
    Function to validate user password
    :param password: takes in password and validates it
    :return: validated password
    """

    SpecialSymbol = ['$', '@', '#', '%']

    if len(password) < 6:
        raise ValidationError(PASSWORD_SHORT_LENGTH_ERROR)

    if len(password) > 20:
        raise ValidationError(PASSWORD_LONG_LENGTH_ERROR)

    if not any(char.isdigit() for char in password):
        raise ValidationError(PASSWORD_CONTAINS_NO_DIGIT_ERROR)

    if not any(char.isupper() for char in password):
        raise ValidationError(PASSWORD_CONTAINS_NO_UPPERCASE_ERROR)

    if not any(char.islower() for char in password):
        raise ValidationError(PASSWORD_CONTAINS_NO_LOWERCASE_ERROR)

    if not any(char in SpecialSymbol for char in password):
        raise ValidationError(PASSWORD_CONTAINS_NO_SPECIAL_CHARACTER_ERROR)
    return password


def validate_date(date_string):
    """
    Function to validate the username
    :param: takes in date parameter and validates it
    :return: validated date
    """
    date_format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(date_string, date_format)
    except Exception as e:
        raise ValidationError(DATE_ERROR)


def validate_price(price):
    if not price.isdecimal():
        raise ValidationError(PRICE_ERROR)
    return price



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