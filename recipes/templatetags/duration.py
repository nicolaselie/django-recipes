# -*- coding: UTF-8 -*-

import datetime

from django import template
from django.utils.html import avoid_wrapping
from django.utils.translation import ugettext, ungettext_lazy

register = template.Library()

@register.filter
def naturalduration(value):
    """
    For a timedelta, returns a nicely formatted string, e.g. "10 minutes".
    Units used are years, months, weeks, days, hours, minutes and seconds.
    Microseconds are ignored. Up to two adjacent units will be
    displayed. For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.
    Adapted from django's timesince default filter.
    """
    
    if not isinstance(value, datetime.timedelta):
        return value
    
    chunks = (
        (60 * 60 * 24 * 365, ungettext_lazy('%d year', '%d years')),
        (60 * 60 * 24 * 30, ungettext_lazy('%d month', '%d months')),
        (60 * 60 * 24 * 7, ungettext_lazy('%d week', '%d weeks')),
        (60 * 60 * 24, ungettext_lazy('%d day', '%d days')),
        (60 * 60, ungettext_lazy('%d hour', '%d hours')),
        (60, ungettext_lazy('%d minute', '%d minutes')),
        (1, ungettext_lazy('%d second', '%d seconds'))
    )

    # ignore microseconds
    since = value.days * 24 * 60 * 60 + value.seconds
    
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
        
    result = avoid_wrapping(name % count)
    if i + 1 < len(chunks):
        # Now get the second item
        seconds2, name2 = chunks[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            result += ugettext(', ') + avoid_wrapping(name2 % count2)
    return result
    