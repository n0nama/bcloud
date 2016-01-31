 # -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
   
    #/tickets/
    url (r'^$', 'ticketracker.views.complain', name = 'ticketracker_complain'),
    #tickets/add_ticket/
    url (r'^add_ticket/$', 'ticketracker.views.add_ticket'),                       
)