from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from messag.views import *

urlpatterns = patterns('',
    url(r'^test/', Inbox.as_view()),
    url(r'^$', RedirectView.as_view(url='inbox/'), name='messages_redirect'),
    url(r'^inbox/$', login_required(Inbox.as_view()), name='messages_inbox'),
    url(r'^outbox/$', Outbox.as_view(), name='messages_outbox'),
    url(r'^favorite/$', Favorite.as_view(), name='messages_favorite'),
    url(r'^compose/$', compose, name='messages_compose'),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', view, name='messages_detail'),
    url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
    url(r'^add_favorite/(?P<message_id>[\d]+)/$', add_favorite, name='message_add_favorite'),
    url(r'^delete_favorite/(?P<message_id>[\d]+)/$', delete_favorite, name='message_delete_favorite'),
    url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
    url(r'^trash/$', Trash.as_view(), name='messages_trash'),
    url(r'^draft_compose/$', compose_draft, name='message_draft_compose'),
    url(r'^draft/$', Draft.as_view(), name='messages_draft'),
    url(r'^delete_draft/(?P<draft_id>[\d]+)/$', delete_draft, name='draft_delete'),
    url(r'^draft_send/(?P<draft_id>[\d]+)/$', draft_send, name='draft_send'),
)
