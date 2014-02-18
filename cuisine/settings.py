"""
Django settings for cuisine project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_98x54!y6d4uj9^2l5ot$xx_@^oz#3@w&6n!i4eco)e0h(e(3i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

APPEND_SLASH = True

ADMINS = (
  ('Nicolas ELIE', 'nicolaselie@free.fr'),
)

SITE_ID = 1


# Application definition

# -*- coding: UTF-8 -*-

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'easy_thumbnails',
    'pagedown',
    'ratings',
    'django.contrib.comments',
    'django.contrib.sites',
    'haystack',
    'recipes',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'recipes.context_processors.available_filters',
)

ROOT_URLCONF = 'cuisine.urls'

WSGI_APPLICATION = 'cuisine.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr_FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media files
MEDIA_URL = '/'

#Templates
TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, 'templates')
)

#User management
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

#Recipes
RECIPES_PAGINATE_BY = 10

#easy-thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'thumbnail': {'size': (240, 180), 'autocrop': True, 'crop': 'smart'},
    },
}

#Ratings
RATINGS_RANGE = (1, 5)

COMMENTS_APP = 'recipes'

# Haystack configuration
HAYSTACK_CONNECTIONS = {
    'default': {
    'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
    'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}