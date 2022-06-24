from django.urls import path

from chat.views import UserValidationView, GetReceiverList

urlpatterns = [
    path('receivers/', GetReceiverList.as_view(), name='receivers'),
    path('user_validation/', UserValidationView.as_view(), name='user_validation')
]

