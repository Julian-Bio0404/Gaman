"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='9_bqs58ror+16_4p-05j5#t77s(c#wmh7(&z$xk3oua#l_#1h%')
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405
