from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserChangePasswordView
    # , UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
]