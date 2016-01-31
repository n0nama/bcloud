# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from haystack.utils import get_model_ct
from haystack.forms import SearchForm
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text


def model_choices(using=DEFAULT_ALIAS):
    choices = [(get_model_ct(m), capfirst(smart_text(m._meta.verbose_name_plural)))
               for m in connections[using].get_unified_index().get_indexed_models()]
    return sorted(choices, key=lambda x: x[1])


class SampleForm(SearchForm):
	
	def __init__(self, *args, **kwargs):
		super(SampleForm, self).__init__(*args, **kwargs)
		
	def search(self):
		sqs = super(SampleForm, self).search()
		
		if not self.is_valid():
			return self.no_query_found()
		
		#sqs = sqs.exclude(content=u'Данила')
		
		return sqs
