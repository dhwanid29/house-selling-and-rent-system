from django.contrib.auth import authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from constants import USER_CREATED, LOGGED_IN, INVALID_EMAIL_OR_PASSWORD, PASSWORD_CHANGED, PASSWORD_RESET_LINK, \
    PASSWORD_RESET_SUCCESSFUL, HOST_URL, EMAIL_BODY_EMAIL_UPDATE, EMAIL_SUBJECT_EMAIL_UPDATE, EMAIL_UPDATE_LINK
from .models import User
from .renderers import UserRenderer
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserChangePasswordSerializer, \
    SendPasswordResetEmailSerializers, \
    UserPasswordResetSerializer, UserProfileSerializer, UserProfileUpdateSerializer, UserEmailUpdateSerializer, \
    ResendEmailUpdateLinkSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Generate token manually
from .utils import EmailSend


def get_tokens_for_user(user):
    """
    Function to get token of the authenticated user
    :param user: takes in user login detail (email)
    :return: two types of token i.e refresh token and access token
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """
    View for User Registration
    """

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'data': serializer.data, 'msg': USER_CREATED},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    View for User Login View
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': LOGGED_IN}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': [INVALID_EMAIL_OR_PASSWORD]}},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    """
    User Profile View
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        try:
            return User.objects.get(id=request.user.id)

        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        user = self.get_object(request)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.get_object(request)
        old_email = user.email
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            if old_email != user.email:
                uid = urlsafe_base64_encode(force_bytes(str(user.id)))
                token = default_token_generator.make_token(user)
                link = HOST_URL + '/email_update/' + uid + '/' + token
                # Send Mail
                body = EMAIL_BODY_EMAIL_UPDATE + link
                data = {
                    'subject': EMAIL_SUBJECT_EMAIL_UPDATE,
                    'body': body,
                    'to_email': user.email
                }
                EmailSend.send_email(data)

            return Response({'msg': EMAIL_UPDATE_LINK, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResendLinkEmailUpdate(APIView):
    """
    Resend Email Update Link
    """

    def post(self, request):
        serializer = ResendEmailUpdateLinkSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'msg': EMAIL_UPDATE_LINK}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    """
    User Change Password View
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'msg': PASSWORD_CHANGED}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    """
    View to get email from user and send reset password link to that mail
    """

    def post(self, request):
        serializer = SendPasswordResetEmailSerializers(data=request.data)
        if serializer.is_valid():
            return Response({'msg': PASSWORD_RESET_LINK}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    """
    View to reset user password
    """

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid():
            return Response({'msg': PASSWORD_RESET_SUCCESSFUL}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailUpdateLoginView(APIView):
    """
    View to reset user password
    """

    def post(self, request, uid, token):
        serializer = UserEmailUpdateSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': LOGGED_IN}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': [INVALID_EMAIL_OR_PASSWORD]}},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
