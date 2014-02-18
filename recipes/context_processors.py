# -*- coding: UTF-8 -*-
from .models import Source, Category
        
def available_filters(request):
    return {'available_categories': Category.objects.all(),
            'available_sources': Source.objects.all()}
