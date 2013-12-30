# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, include, url
from recipes.views import RecipesListView, ListRecipesByDate, \
                          ListRecipesByCategory, RecipeView, \
                          RecipesMonthArchiveView

urlpatterns = patterns('recipes.views',
    url(r'^$', RecipesListView.as_view(), name='home'),
    
    # Recipe detail by pk
    url(r'^recpe/(?P<pk>\d+)/$',
        RecipeView.as_view(),
        name='recipe_by_pk'),
    # Recipe detail by slug
    url(r'^recipe/(?P<slug>[-\w]+)/$',
        RecipeView.as_view(),
        name='recipe_by_slug'),
    
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$',
        RecipesMonthArchiveView.as_view(month_format='%m'),
        name='recipe_archive_month'),
    # Recipes list by date
    #url(r'^recipes/(?P<year>\d{4})/(?P<month>\d{2})/$',
        #ListRecipesByDate.as_view(),
        #name='list_recipes_by_date'),
    # Recipes list by category
    url(r'^category/(?P<pk>\d+)/$',
        ListRecipesByCategory.as_view(),
        name='list_recipes_by_category'),
)