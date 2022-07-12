from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from accounts.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from accounts.utils import EmailSend
from accounts.validations import validate_password
from constants import PASSWORD_DO_NOT_MATCH, HOST_URL, EMAIL_BODY, EMAIL_SUBJECT, NOT_REGISTERED, INVALID_TOKEN, \
    CURRENT_PASSWORD_CHECK, CURRENT_PASSWORD_AND_CHANGE_PASSWORD_ARE_SAME, EMAIL_BODY_EMAIL_UPDATE, \
    EMAIL_SUBJECT_EMAIL_UPDATE


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for User Registration
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2', 'phone_number', 'address',
                  'profile_image']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError(PASSWORD_DO_NOT_MATCH)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User Profile View
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'profile_image']


class ResendEmailUpdateLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for Resend Email Update View
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            user = User.objects.filter(email=email).first()
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = HOST_URL + '/email_update/' + uid + '/' + token
            # Send Mail
            body = EMAIL_BODY_EMAIL_UPDATE + link
            data = {
                'subject': EMAIL_SUBJECT_EMAIL_UPDATE,
                'body': body,
                'to_email': user.email
            }
            EmailSend.send_email(data)
            return attrs
        except:
            raise ValidationError(NOT_REGISTERED)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for User Profile View
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'profile_image']

    def validate_email(self, value):
        if self.instance and value != self.instance.email:
            return value


class UserEmailUpdateSerializer(serializers.Serializer):
    """
    Serializer to Login Again after updating email
    """
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'}, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        try:
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not default_token_generator.check_token(user, token):
                raise ValidationError(INVALID_TOKEN)
            return attrs
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError(INVALID_TOKEN)


class UserChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for User Change Password
    """
    current_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if not check_password(current_password, user.password):
            raise serializers.ValidationError(CURRENT_PASSWORD_CHECK)
        if current_password == password and current_password == password2:
            raise serializers.ValidationError(CURRENT_PASSWORD_AND_CHANGE_PASSWORD_ARE_SAME)
        if password != password2:
            raise serializers.ValidationError(PASSWORD_DO_NOT_MATCH)
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializers(serializers.Serializer):
    """
    Serializer to get email from user and send password reset link to user via mail
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = HOST_URL + '/reset-password/' + uid + '/' + token
            # Send Mail
            body = EMAIL_BODY + link
            data = {
                'subject': EMAIL_SUBJECT,
                'body': body,
                'to_email': user.email
            }
            EmailSend.send_email(data)
            return attrs
        else:
            raise ValidationError(NOT_REGISTERED)


class UserPasswordResetSerializer(serializers.Serializer):
    """
    Serializer to Reset Password
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(PASSWORD_DO_NOT_MATCH)
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError(INVALID_TOKEN)
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError(INVALID_TOKEN)
