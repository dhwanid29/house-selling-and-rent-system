from audioop import reverse

import jwt
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import User
from chat.models import Message
from house.models import House
from house_selling import settings


class UserValidationView(View):

    def get(self, request):
        return render(request, template_name='chat/user_validation.html')

    def post(self, request):
        token = request.POST['token']
        valid_data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        print(valid_data, '------------------------------------------------------------------------------->')
        validated_user = valid_data['user_id']
        del request.session['user_id']
        request.session.modified = True
        request.session['user_id'] = validated_user
        return redirect('receivers')


class CreateRoom(View):

    def get(self, request):
        queryset = House.objects.all().distinct('user')
        return render(request, 'chat/select_receiver.html', {'context': queryset})

    def post(self, request):
        sender = request.session.get("user_id")
        sender_user = User.objects.get(id=sender)
        receiver = request.POST['receivers']
        receiver_user = User.objects.get(id=receiver)
        room_name = f"{sender}_and_{receiver}"
        room = f"{receiver}_and_{sender}"
        get_all_rooms = Message.objects.filter(Q(room_name=room_name) | Q(room_name=room))
        if get_all_rooms:
            return HttpResponse('Room exists')
        else:
            create_room = Message.objects.create(sender=sender_user, receiver=receiver_user, room_name=room_name)
            create_room.save()
            return HttpResponse(request.POST['receivers'])

