from __future__ import unicode_literals

try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from haystack.views import SearchView

from haystack.forms_custom import SampleForm
from haystack.views import SearchView, search_view_factory


urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
				view_class= SearchView,
				template='search/search.html',
				#template='friendship/templates/user_actions.html',
				#searchqueryset=sqs,
				form_class=SampleForm,
				), name='haystack_search'),
)
