from rest_framework import serializers
from accounts.models import User
from phonenumber_field.formfields import PhoneNumberField

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile_image = serializers.ImageField(required=False)
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields=['fname', 'lname', 'username', 'email', 'password', 'password2', 'phone_number', 'address', 'profile_image']
        # extra_kwargs={
        #     'password':{'write_only': True}
        # }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match!")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name']