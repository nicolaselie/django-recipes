# -*- coding: UTF-8 -*-

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, MonthArchiveView

import re

from recipes.models import Recipe

#ALLOWED_UNITS = ['°C', 'h', 'min', 's', 'g', 'mg', 'cg', 'L', 'mL', 'cL', 'dL', 'verre']

## blah + number + 0 or 1 space + allowed unit + end of line or non alphanumeric character
#UNITS_RE = re.compile('(?P<value>[0-9]+)\s{0,1}(?P<unit>%s)(?=$|[^a-zA-Z]+)' 
                        #% '|'.join(ALLOWED_UNITS))
# blah + number + / + number
FRAC_RE = re.compile('(?P<numerator>[0-9]+)/(?P<denominator>[0-9]+)')

def sub_frac(g):
    return r'<sup>%s</sup>&frasl;<sub>%s</sub>' % (g.group('numerator'), g.group('denominator'))

class Ingredient:
    def __init__(self, name, quantity):
        self.name = name.strip()
        self.quantity = quantity.strip()

###
# Views
###

class RecipesGeneric:
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 4

class RecipesListView(RecipesGeneric, ListView):
    """List all recipes"""
    pass

class RecipesMonthArchiveView(RecipesGeneric, MonthArchiveView):
    """List all recipes corresponding to the current month and year"""
    date_field = "modification_time"
    make_object_list = True
    allow_future = True
    #allow_empty = True

class ListRecipesByDate(RecipesListView):
    """List all recipes corresponding to the current month and year"""
    def get_queryset(self):
        year, month = self.kwargs['year'], self.kwargs['month']
        return Recipe.objects.filter(modification_time__year=year, 
                                     modification_time__month=month)
    
class ListRecipesByCategory(RecipesListView):
    """List all recipes in the selected category"""
    def get_queryset(self):
        pk = self.kwargs['id']
        return Recipe.objects.filter(category=pk)

class RecipeView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    
    def get_context_data(self, **kwargs):
        context = super(RecipeView, self).get_context_data(**kwargs)
        recipe = context['recipe']
        
        ingredients = []
        for line in recipe.ingredients.split('\n'):
            line = line.strip()
            line = FRAC_RE.sub(sub_frac, line)
            if ':' in line:
                l = line.split(':')
                ingred = Ingredient(name=l[0], quantity=l[1])
            else:
                ingred = Ingredient(name=line, quantity="")
            ingredients.append(ingred)
        
        steps = []
        for line in recipe.content.split('\n'):
            line = line.strip()
            #line = UNITS_RE.sub(sub_units, line)
            line = FRAC_RE.sub(sub_frac, line)
            steps.append(line)
        
        context['ingredients'] = ingredients
        context['steps'] = steps
        
        return context
