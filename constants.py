from house_selling import settings

# ACCOUNTS SERIALIZER
if settings.DEBUG:
    HOST_URL = "http://127.0.0.1:8000/api/user"
else:
    HOST_URL = "https://house-selling-and-rent-system.herokuapp.com/api/user"

# ACCOUNTS SERIALIZER

PASSWORD_DO_NOT_MATCH = "Password and Confirm Password doesn't match"
EMAIL_BODY = "Click Following Link to Reset Your Password "
EMAIL_SUBJECT = "Reset Your Password"
NOT_REGISTERED = "You are not a registered user."
INVALID_TOKEN = "Token is not Valid or Expired."
CURRENT_PASSWORD_CHECK = "Current password is invalid"

# ACCOUNTS VIEW

USER_CREATED = "User Created Successfully!"
LOGGED_IN = "Login Successfully!"
INVALID_EMAIL_OR_PASSWORD = "Email or Password is not valid"
PASSWORD_CHANGED = "Password Changed Successfully!"
PASSWORD_RESET_LINK = "Password Reset link send. Please check your Email"
PASSWORD_RESET_SUCCESSFUL = "Password Reset Successfully"

# ACCOUNTS VALIDATIONS

PASSWORD_VALIDATION_ERROR = "Invalid password. Password must contain atleast one uppercase alphabet, one lowercase alphabet, one digit, one special character and must be 8 to 20 characters in length."
USERNAME_SHORT_ERROR = "Username too short.Please enter a username of atleast 3 characters."
USERNAME_LONG_ERROR = "Username too long.Please enter a username of not greater than 30 characters."
ONLY_LOWERCASE = "Username should consists of lower case alphabets only."
NO_SPACES_ALLOWED = "Username cannot contain spaces."
NAME_NO_SPACES_ALLOWED = "Name cannot contain spaces."
INVALID_NAME = "This name is invalid. Enter a valid name"

# ACCOUNTS MANAGER

EMAIL_REQUIRED = 'Users must have an email address'


# HOUSE VIEW
NO_ACCESS_UPDATE_REVIEW = "You do not have access to this update this review."
NO_ACCESS_UPDATE_HOUSE_IMAGE = "You do not have rights to update these images."