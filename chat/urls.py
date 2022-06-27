from django.urls import path

from chat.views import UserValidationView, CreateRoom, ChatRoom

urlpatterns = [
    path('receivers/', CreateRoom.as_view(), name='receivers'),
    path('user_validation/', UserValidationView.as_view(), name='user_validation'),
    path('<str:room_name>/', ChatRoom.as_view(), name='room')
]

