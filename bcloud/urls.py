from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
import users.views as views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bcloud.views.home', name='home'),
    url('', include('allauth.urls')),
    url(r'^dashboard', 'bcloud.views.dashboard', name='dashboard'),
    url(r'^chat/', include('chat.urls')),
    url(r'^admin/cp', 'bcloud.admin.dash'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^messages/', include('messag.urls')),
    url(r'^profile', 'users.views.profile', name='profile'),
    url(r'^portfolio', views.PortfolioCreate.as_view()),
    url(r'^users$', 'friendship.views.all_users'),
    url(r'^search/', include('haystack.urls')),
    url(r'^projects/', include('projects.urls', namespace='projects', app_name='projects')),
    #url('', include('friendship.urls')),
    url(r'^notifications/', include('notifications.urls')),

    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url('', include('news.urls', namespace='news')),
)

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)