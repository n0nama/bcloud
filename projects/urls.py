from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',

    url(r'^$', 
        views.all_projects, 
        name='all_projects'),

    url(r'^myprojects/$', 
        views.my_projects, 
        name='my_projects'),

    url(r'^(?P<project_id>\d+)/$', 
        views.get_project, 
        name='getProject'),
    
    url(r'^create_project/$', 
        views.create_project, 
        name='createProject'),
    
    url(r'^edit/(?P<project_id>\d+)/$', 
        views.edit_project, 
        name='editProject'),
    
    url(r'^reply/(?P<project_id>\d+)/$', 
        views.make_reply, 
        name='make_reply'),
    
    url(r'reply/(?P<project_id>\d+)/(?P<reply_id>\d+)/$', 
        views.reply_details, 
        name='replyDetails'),

)