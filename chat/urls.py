from django.conf.urls import patterns, url
from chat.views import *

urlpatterns = patterns('',
    url(r'^$', chat, name = 'chat'),
    url(r'^send_message/$', send_message, name = 'send'),
    url(r'^get_history/$', get_history, name = 'history'),
)