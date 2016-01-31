from django.http import HttpResponse
from chat.models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from friendship.models import Friend
from users.models import Profile
from django.utils.crypto import get_random_string
import redis
import json


@login_required
def chat(request):
    user = ChatUser.objects.get(user=request.user)
    friends = Friend.objects.friends(request.user)
    dialogs = user.dialogs.all()
    friends_list = {}

    for friend in friends:
        chat_friend = ChatUser.objects.get(user=friend)
        prof = Profile.objects.get(user=friend)
        name = prof.f_name + ' ' + prof.l_name
        try:
            friends_list[name] = room.objects.filter(users=user, room_name='').filter(users=chat_friend)[0].room_id
        except:
            r = room()
            r.save()
            r.set_id()
            r.users.add(chat_friend)
            r.users.add(user)
            r.save()
            friends_list[name] = r.room_id
    return render_to_response('chat/chat.html',
                              {'username': request.user.username, 'dialogs': dialogs, 'friends': friends_list})

@csrf_exempt
@login_required
@require_POST
def send_message(request):
    if 'message' not in request.POST:
        return HttpResponse('Enter message')
    if 'room_id' not in request.POST:
        return HttpResponse('Enter room')

    try:
        room_id = request.POST['room_id']
        text = request.POST['message']
        sender = ChatUser.objects.get(user=request.user)
        chat_room = room.objects.get(room_id=room_id)
        if chat_room.room_name == '':
            receiver = chat_room.users.all().exclude(user=request.user)[0]
            if request.user not in Friend.objects.friends(User.objects.get(username = receiver.user.username)):
                 return HttpResponse('Access2 denied')
        else:
            if sender not in chat_room.users.all():
                return HttpResponse('Access1 denied')
    except:
        return HttpResponse('Error')

    m = message(sender=sender, room=chat_room, text=text)
    m.save()
    redis_message = json.dumps({'text': m.text, 'sender': m.sender.user.username, 'date': m.get_date(), 'name': m.get_fname()})

    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    r.publish(room_id, redis_message)

    return HttpResponse()

@login_required
@csrf_exempt
def get_history(request):
    if request.method != "POST":
        return HttpResponse('Error')
    if 'room_id' not in request.POST:
        return HttpResponse('Enter room')
    if 'last_message' not in request.POST:
        return HttpResponse('Error')

    try:
        last = request.POST['last_message']
        room_id = request.POST['room_id']
        username = request.user.username
        chat_room = room.objects.get(room_id=room_id)
        user = ChatUser.objects.get(user=request.user)
        messages = message.objects.filter(room=chat_room)
        r = redis.StrictRedis(host='127.0.0.1', port=6379)
        auth_key = get_random_string(16)
        r.set(chat_room.room_id, auth_key)
    except 'DoesNotExist':
        return HttpResponse('Error')
    message_list = []
    if len(messages) == 0 or last == messages.reverse()[0].text:
        return render_to_response('chat/history.html', {'messages': message_list, 'id': room_id, 'key': auth_key})

    for m in messages.reverse():
        if m.text != last:
            message_list.append(m)
        else:
            break
    message_list.reverse()

    return render_to_response('chat/history.html', {'messages': message_list, 'id': room_id, 'key': auth_key})

def create_conference(request):
    if not request.user.is_authenticated():
        return HttpResponse('Please login')
    user = ChatUser.objects.get(user=request.user)

    if request.method == "GET":
        friends = user.friends.all()

        return render_to_response('chat/create_conference.html', {'friends': friends})

    if request.method == "POST":
        if 'room_name' not in request.POST or request.POST['room_name'] == '':
            return HttpResponse('Enter room name')
        if len(request.POST) < 3:
            return HttpResponse('Minimal 3 users in room')

        r = room(room_name=request.POST['room_name'])
        r.set_id()
        r.save()
        r.users.add(user)
        user.dialogs.add(r)
        for key, value in request.POST.iteritems():
            if key == 'room_name': continue
            r.users.add(ChatUser.objects.get(username=key))
            ChatUser.objects.get(username=key).dialogs.add(r)

        return HttpResponse("OK")