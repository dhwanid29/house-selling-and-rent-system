from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from constants import USER_CREATED, LOGGED_IN, INVALID_EMAIL_OR_PASSWORD, PASSWORD_CHANGED, PASSWORD_RESET_LINK, \
    PASSWORD_RESET_SUCCESSFUL
from .models import User
from .renderers import UserRenderer
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializers,\
    UserPasswordResetSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Generate token manually
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
        print("request.data", request.data, type(request.data))
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': USER_CREATED}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    View for User Login View
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': LOGGED_IN}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': [INVALID_EMAIL_OR_PASSWORD]}}, status=status.HTTP_404_NOT_FOUND)


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
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserChangePasswordView(APIView):
    """
    User Change Password View
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': PASSWORD_CHANGED}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    """
    View to get email from user and send reset password link to that mail
    """
    def post(self, request):
        serializer = SendPasswordResetEmailSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': PASSWORD_RESET_LINK}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    """
    View to reset user password
    """

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': PASSWORD_RESET_SUCCESSFUL}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
