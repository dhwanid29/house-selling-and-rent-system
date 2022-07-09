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
CURRENT_PASSWORD_AND_CHANGE_PASSWORD_ARE_SAME = "Old password and new password are same"

# ACCOUNTS VIEW

USER_CREATED = "User Created Successfully!"
LOGGED_IN = "Login Successfully!"
INVALID_EMAIL_OR_PASSWORD = "Email or Password is not valid"
PASSWORD_CHANGED = "Password Changed Successfully!"
PASSWORD_RESET_LINK = "Password Reset link send. Please check your Email"
PASSWORD_RESET_SUCCESSFUL = "Password Reset Successfully"
LIKE_ERROR = "You have already liked this house"
DISLIKE_ERROR = "You have not liked this house"
FAVOURITE_ERROR = "You have already added this house to favourites"
REMOVE_FAVOURITES_ERROR = "You haven't added this house to favourites"

# ACCOUNTS VALIDATIONS

PASSWORD_VALIDATION_ERROR = "Invalid password. Password must contain atleast one uppercase alphabet, one lowercase alphabet, one digit, one special character and must be 8 to 20 characters in length."
USERNAME_SHORT_ERROR = "Username too short.Please enter a username of atleast 3 characters."
USERNAME_LONG_ERROR = "Username too long.Please enter a username of not greater than 30 characters."
ONLY_LOWERCASE = "Username should consists of lower case alphabets only."
NO_SPACES_ALLOWED = "Username cannot contain spaces."
NAME_NO_SPACES_ALLOWED = "Name cannot contain spaces."
INVALID_NAME = "This name is invalid. Enter a valid name"
PASSWORD_SHORT_LENGTH_ERROR = "length should be at least 6"
PASSWORD_LONG_LENGTH_ERROR = "length should be not be greater than 8"
PASSWORD_CONTAINS_NO_DIGIT_ERROR = "Password should have at least one numeral"
PASSWORD_CONTAINS_NO_UPPERCASE_ERROR = "Password should have at least one uppercase letter"
PASSWORD_CONTAINS_NO_LOWERCASE_ERROR = "Password should have at least one lowercase letter"
PASSWORD_CONTAINS_NO_SPECIAL_CHARACTER_ERROR = "Password should have at least one of the symbols $@#"

# ACCOUNTS MANAGER

EMAIL_REQUIRED = 'Users must have an email address'


# HOUSE VIEW
NO_ACCESS_UPDATE_REVIEW = "You do not have access to update this review."
NO_ACCESS_UPDATE_HOUSE_IMAGE = "You do not have rights to update these images."
EMAIL_BODY_FAVOURITES = "Your House is Shortlisted by someone."
EMAIL_SUBJECT_FAVOURITES = "Contact this user ->"
HOUSE_DOES_NOT_EXIST = "This house doesn't exist"
HOUSE_CREATED = "House data submitted successfully"
HOUSE_UPDATED = "House data updated successfully"
REVIEW_CREATED = "Review submitted successfully"
REVIEW_ALREADY_CREATED = "Review is already submitted"
REVIEW_UPDATED = "Review updated successfully"
LIKED = "You liked the house"
UNLIKED = "You unliked the house"
ADDED_TO_FAVOURITES = "House added to favourites"
REMOVED_FAVOURITES = "House removed from favourites"
PREFERENCE_CREATED = "Preference created successfully"
PREFERENCE_ALREADY_CREATED = "Preference already created"
PREFERENCE_UPDATED = "Preference updated successfully"
NO_ACCESS_UPDATE_PREFERENCE = "You do not have rights to update these preferences."
DATA_RETRIEVED = "Data Retrieved Successfully"
EMAIL_SUBJECT_FAV_SELLER = "Your favourite seller has posted a new House."
EMAIL_BODY_FAV_SELLER = "View the house"
AMENITIES_CREATED = "Added Successfully"
AMENITIES_UPDATED = "Updated Successfully"
AMENITIES_DELETE = "Deleted Successfully"
AMENITIES_VIEW = "Retreived Successfully"