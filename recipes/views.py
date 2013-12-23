# -*- coding: UTF-8 -*-

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

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

def list_recipes(request, recipes):
    """Render a list of selected recipes"""
    return render(request, 'recipes/recipes.html', {'recipes': recipes})

###
# Views
###

class ListRecipes(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "recipes/recipes.html"
    paginate_by = 5

def list_recipes_by_date(request, month, year):
    """List all recipes corresponding to the current month and year"""
    recipes = Recipe.objects.filter(date__year=year, 
                                    date__month=month)
    return list_recipes(request, recipes)

def list_recipes_by_category(request, id):
    """List all recipes in the selected category"""
    recipes = Recipe.objects.filter(category=id)
    return list_recipes(request, recipes)

def home(request):
    """Homepage, list all recipes"""
    return list_recipes(request, Recipe.objects.all())

def view_recipe(request, id):
    """ Render a recipe from it's id """
   
    recipe = get_object_or_404(Recipe, id=id)
    
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
    
    data = {'recipe': recipe,
            'ingredients': ingredients,
            'steps': steps}
    return render(request, 'recipes/recipe.html', data)
