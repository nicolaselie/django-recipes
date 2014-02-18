# -*- coding: UTF-8 -*-

from django import template
from django.db.models.query import QuerySet

register = template.Library()

@register.filter
def find_query(value, arg):
    if isinstance(value, QuerySet):
        result = []
        for q in value:
            if arg.lower() in q.slug or arg.lower() in q.name.lower():
                result.append(q)
        return result
    else:
        return value