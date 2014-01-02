# -*- coding: UTF-8 -*-

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, MonthArchiveView
from django.conf import settings

import re

from recipes.models import Recipe, Source

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

class RecipesMixin(object):
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 4

class RecipesListView(RecipesMixin, ListView):
    """List all recipes filtered by category, author, difficulty, cost"""
    
    def get_queryset(self):
        if 'category' in self.kwargs:
            slug = self.kwargs['category']
            return Recipe.objects.filter(category__slug=slug)
        elif 'author' in self.kwargs:
            author = self.kwargs['author']
            return Recipe.objects.filter(author__username=author)
        elif 'difficulty' in self.kwargs:
            difficulty = self.kwargs['difficulty']
            return Recipe.objects.filter(difficulty=difficulty)
        elif 'cost' in self.kwargs:
            cost = self.kwargs['cost']
            return Recipe.objects.filter(cost=cost)
        if 'source' in self.kwargs:
            source = self.kwargs['source']
            return Recipe.objects.filter(sources__slug=source)
        else:
            return Recipe.objects.all()
            
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        if 'category' in self.kwargs and context['object_list']:
            context['category'] = context['object_list'][0].category.name
        elif 'author' in self.kwargs:
            context['author'] = self.kwargs['author']
        elif 'difficulty' in self.kwargs and context['object_list']:
            context['difficulty'] = context['object_list'][0].get_difficulty()
        elif 'cost' in self.kwargs and context['object_list']:
            context['cost'] = context['object_list'][0].get_cost()
        elif 'source' in self.kwargs and context['object_list']:
            slug = self.kwargs['source']
            source = Source.objects.filter(slug=slug)
            if source:
                source = source[0]
            context['source'] = source
        
        return context
        
class RecipesMonthArchiveView(RecipesMixin, MonthArchiveView):
    """List all recipes corresponding to the current month and year"""
    template_name = "recipes/recipe_list.html"
    date_field = "modification_time"
    make_object_list = True
    allow_future = True
    
    def get_allow_empty(self):
        if settings.DEBUG:
            return True
        else:
            return super(MonthArchiveView, self).get_allow_empty()
            
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
