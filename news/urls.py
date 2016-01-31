from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^news/$', views.news_list, name='NewsList'),
    url(r'^news/(?P<new_id>[0-9]+)$', views.single_new, name='single_new'),
)