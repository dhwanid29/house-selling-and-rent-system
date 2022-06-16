from house_selling import settings

if settings.DEBUG:
    host_url = "http://127.0.0.1:8000/api/user"
else:
    host_url = "https://house-selling-and-rent-system.herokuapp.com/api/user"

# serializer messages

password_do_not_match = "Password and Confirm Password doesn't match"
email_body = "Click Following Link to Reset Your Password "
email_subject = "Reset Your Password"
not_registered = "You are not a registered user."
invalid_token = "Token is not Valid or Expired."
CURRENT_PASSWORD_CHECK = "Current password is invalid"

# views messages

user_created = "User Created Successfully!"
logged_in = "Login Successfully!"
invalid_email_or_password = "Email or Password is not valid"
password_changed = "Password Changed Successfully!"
password_reset_link = "Password Reset link send. Please check your Email"
password_reset_successful = "Password Reset Successfully"

# validations messages

password_validation_error = "Invalid password. Password must contain atleast one uppercase alphabet, one lowercase alphabet, one digit, one special character and must be 8 to 20 characters in length."
username_short_error = "Username too short.Please enter a username of atleast 3 characters."
username_long_error = "Username too long.Please enter a username of not greater than 30 characters."
only_lowercase = "Username should consists of lower case alphabets only."
no_spaces_allowed = "Username cannot contain spaces."
name_no_spaces_allowed = "Name cannot contain spaces."
invalid_name = "This name is invalid. Enter a valid name"

# managers messages

email_required = 'Users must have an email address'