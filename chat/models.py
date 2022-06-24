from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import SET

from accounts.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='sender')
    receiver = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='receiver')
    message = models.TextField()
    room_name = models.CharField(max_length=255, unique=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)