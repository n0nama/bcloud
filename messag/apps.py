from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DjangoMessagesConfig(AppConfig):
    name = 'messag'
    verbose_name = _('Messages')
