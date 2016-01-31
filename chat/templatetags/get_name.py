from django.template import Library
from django.utils.safestring import mark_safe
import json

register = Library()

@register.filter(is_safe=True)
def get_name(obj, epk):
    return mark_safe(json.dumps(obj.get_sender_name(epk)))