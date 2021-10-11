"""Production settings."""

from .local import *

DEBUG = False

# Anymail (Mailgun)
INSTALLED_APPS += ['anymail']
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
ANYMAIL = {
    'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_DOMAIN')
}

# Gunicorn
INSTALLED_APPS += ['gunicorn']
