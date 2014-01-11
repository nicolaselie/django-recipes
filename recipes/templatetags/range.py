# -*- coding: UTF-8 -*-

from django import template

register = template.Library()

@register.filter(name='range')
def drange(value, arg=0):
    if not isinstance(value, int):
        return value
    
    return range(arg, value) 
