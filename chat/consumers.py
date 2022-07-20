# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from accounts.models import User
from chat.models import Message


class ChatConsumer(WebsocketConsumer):
    # save message in database
    def message_save(self, message, sender, receiver):
        sender_user = User.objects.get(id=sender)
        receiver_user = User.objects.get(id=receiver)
        msg = Message.objects.create(sender=sender_user, receiver=receiver_user, message=message)
        msg.save()

    # Connection with websocket to send and receive msgs
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        sender_name = text_data_json['sender_name']

        self.message_save(message, sender, receiver)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
                'sender_name': sender_name
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        sender_name = event['sender_name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'sender_name': sender_name
        }))
