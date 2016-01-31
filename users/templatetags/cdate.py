import datetime

from django import template
from django.utils.translation import ugettext, ungettext

register = template.Library()


@register.filter(name='cdate')
def humanize_timesince(date):
    delta = datetime.datetime.now() - date

    num_years = delta.days / 365
    if (num_years > 0):
        return ungettext(u"%d year ago", u"%d years ago", num_years) % num_years

    num_weeks = delta.days / 7
    if (num_weeks > 0):
        return ungettext(u"%d week ago", u"%d weeks ago", num_weeks) % num_weeks

    if (delta.days > 0):
        return ungettext(u"%d day ago", u"%d days ago", delta.days) % delta.days

    num_hours = delta.seconds / 3600
    if (num_hours > 0):
        return ungettext(u"%d hour ago", u"%d hours ago", num_hours) % num_hours

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return ungettext(u"%d minute ago", u"%d minutes ago", num_minutes) % num_minutes

    return ugettext(u"just a few seconds ago")
    
@register.filter(name='years')
def years(value):
    """
    Filter - removes the minutes, seconds, and milliseconds from a datetime

    Example usage in template:

    {{ my_datetime|only_hours|timesince }}

    This would show the hours in my_datetime without showing the minutes or seconds.
    """
    #replace returns a new object instead of modifying in place
    return value.replace(months=0)
    
@register.filter
def age(value):
    now = datetime.now()
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}