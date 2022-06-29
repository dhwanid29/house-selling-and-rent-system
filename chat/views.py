from audioop import reverse

import jwt
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from accounts.models import User
from chat.models import Message, Room
from house.models import House
from house_selling import settings


class UserValidationView(View):

    def get(self, request):
        return render(request, template_name='chat/user_validation.html')

    def post(self, request):
        token = request.POST['token']
        valid_data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        validated_user = valid_data['user_id']
        request.session['user_id'] = validated_user
        return redirect('receivers')


class CreateRoom(View):

    def get(self, request):
        sender = request.session.get("user_id")
        queryset = House.objects.all().distinct('user')
        get_rooms = Room.objects.filter(Q(sender=sender) | Q(receiver=sender))
        get_senders = Room.objects.filter(sender=sender)
        get_receivers = Room.objects.filter(receiver=sender)
        return render(request, 'chat/select_receiver.html', {'context': queryset, 'rooms': get_rooms,
                                                             'get_senders': get_senders, 'get_receivers': get_receivers,
                                                             'sender': sender})

    def post(self, request):
        sender = request.session.get("user_id")
        sender_user = User.objects.get(id=sender)
        receiver_id = request.POST['receivers']
        request.session['receiver_id'] = receiver_id
        receiver = request.session.get("receiver_id")
        receiver_user = User.objects.get(id=receiver)
        if int(sender) == int(receiver):
            return HttpResponse('You cannot chat with yourself.')
        room_name = f"{sender}_and_{receiver}"
        room = f"{receiver}_and_{sender}"
        get_all_rooms = Room.objects.filter(Q(room_name=room_name) | Q(room_name=room))
        if get_all_rooms:
            return redirect('room', room_name=get_all_rooms[0])
        else:
            create_room = Room.objects.create(sender=sender_user, receiver=receiver_user, room_name=room_name)
            create_room.save()
            return redirect('room', room_name=room_name)


class ChatRoom(View):
    template_name = 'chat/room.html'

    def get(self, request, room_name, *args, **kwargs):
        sender = request.session.get("user_id")
        room = Room.objects.get(room_name=self.kwargs.get("room_name"))
        get_room = get_object_or_404(Room, room_name=self.kwargs.get('room_name'))
        if room.receiver.id == sender:
            receivers = room.sender.id
        else:
            receivers = room.receiver.id
        request.session['receiver_id'] = receivers
        sender = request.session.get("user_id")
        sender_username_id = User.objects.get(id=sender)
        sender_username = sender_username_id.username
        receiver = request.session.get("receiver_id")
        receiver_username_id = User.objects.get(id=receiver)
        receiver_username = receiver_username_id.username
        msgs = Message.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'sender_id': sender,
            'receiver_id': receiver,
            'msgs': msgs,
            'sender_username': sender_username,
            'receiver_username': receiver_username
        })
