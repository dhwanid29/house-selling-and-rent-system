from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserChangePasswordView, SendPasswordResetEmailView, \
    UserPasswordResetView, UserProfileView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]