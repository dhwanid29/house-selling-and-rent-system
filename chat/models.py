from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import SET
from accounts.models import User


class Room(models.Model):
    """
    Model to create room
    """
    sender = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='sender_room')
    receiver = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='receiver_room')
    room_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    """
    Model to save messages
    """
    sender = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='sender')
    receiver = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
