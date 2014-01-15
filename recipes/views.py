# -*- coding: UTF-8 -*-

from django.views.generic import View, ListView, DetailView, MonthArchiveView
from django.views.generic.edit import FormView
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from class_based_auth_views.views import LoginView, LogoutView

import re
import json

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
# Decorators
###

#http://www.daveoncode.com/2013/10/21/creating-class-based-view-decorators-using-simple-django-function-decorators/
def require_AJAX(View):
    """Decorator to require that a class based view only accept AJAX requests."""
    def ajaxOnly(function):
        def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseForbidden()
            return function(request, *args, **kwargs)
 
        return wrap
 
    View.dispatch = method_decorator(ajaxOnly)(View.dispatch)
    return View

###
# Views
###

class RecipesMixin(object):
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 5
    
    def get_paginate_by(self, queryset):
        if hasattr(settings, 'RECIPES_PAGINATE_BY'):
            return settings.RECIPES_PAGINATE_BY
        else:
            return self.paginate_by

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
            context['difficulty'] = context['object_list'][0].get_difficulty_display()
        elif 'cost' in self.kwargs and context['object_list']:
            context['cost'] = context['object_list'][0].get_cost_display()
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
    
class AjaxableMixin(object):
    """
    Mixin to add AJAX support to a View.
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
        
@require_AJAX
class AjaxLoginFormView(FormView):
    template_name = 'registration/login_fragment.html'
    form_class = AuthenticationForm
 
@require_AJAX
class AjaxLogoutFormView(FormView):
    template_name = 'registration/logout_fragment.html'
    form_class = AuthenticationForm

class AjaxLoginView(AjaxableMixin, LoginView):
    def form_invalid(self, form):
        response = super(AjaxLoginView, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxLoginView, self).form_valid(form)
        
        if self.request.is_ajax():
            username = form.get_user().username
            data = {'username': username,
                    'login': reverse('ajax-login-form'),
                    'logout': reverse('ajax-logout-form'),
                   }
            return self.render_to_json_response(data)
        else:
            return response
        
class AjaxLogoutView(AjaxableMixin, LogoutView):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
            
        if self.request.is_ajax():
            data = {'login': reverse('ajax-login-form'),
                    'logout': reverse('ajax-logout-form'),
                   }
            return self.render_to_json_response(data)
        else:
            return None
