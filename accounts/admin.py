from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_image', 'is_admin', 'profile_image')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'phone_number', 'address', 'profile_image')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'phone_number', 'address', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)


#
# {
# "first_name": "heli",
# "last_name": "shah",
# "username": "heli",
# "email": "heli@gmail.com",
# "password": "123456",
# "password2": "123456",
# "phone_number": "+91 8677778987",
# "address": "gota"
# }