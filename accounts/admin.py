from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'username', 'fname', 'lname', 'email', 'phone_number', 'address', 'profile_image', 'is_admin', 'profile_image')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fname', 'lname', 'username', 'phone_number', 'address', 'profile_image')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('fname', 'lname', 'username', 'email', 'phone_number', 'address', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)


#
# {
# "fname": "heli",
# "lname": "shah",
# "username": "heli",
# "email": "heli@gmail.com",
# "password": "123456",
# "password2": "123456",
# "phone_number": "+91 8677778987",
# "address": "gota"
# }