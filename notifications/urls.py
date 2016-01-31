from django.conf.urls import patterns, url
from notifications.views import *

urlpatterns = patterns('',
    url(r'^get_notification/$', get_notification_info, name='get_notification_info'),
    url(r'^read_notification/$', read_notification, name='read_notification'),
    url(r'^get_last/$', get_unread_notifications, name='get_unread_notifications'),
)