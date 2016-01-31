from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json

from notifications.models import Notification


@csrf_exempt
@login_required
def get_notification_info(request):
    if 'id' in request.POST:
        notification = get_object_or_404(Notification, id=request.POST['id'])

        if notification.user != request.user:
            return HttpResponseForbidden('Error')

        return HttpResponse(json.dumps(notification.serialize()))
    else:
        return HttpResponse('Error')


@csrf_exempt
@login_required
def read_notification(request):
    if 'id' in request.POST:
        notification = get_object_or_404(Notification, id=request.POST['id'])

        if notification.user != request.user:
            return HttpResponseForbidden('Error')

        notification.delete()

        return HttpResponse()
    else:
        return HttpResponse('Error')


@csrf_exempt
@login_required
def get_unread_notifications(request):
    user = request.user

    if request.method == "POST":
        notifications = Notification.objects.filter(user=user)[:5]
        response = []

        for n in notifications:
            response.append(n.serialize())

        return HttpResponse(json.dumps(response))

    else:
        notifications = Notification.objects.filter(user=user)
        response = []

        for n in notifications:
            response.append(n.serialize)

        return render_to_response('notifications.html', {'notifications': response})