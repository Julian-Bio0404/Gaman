"""Django settings for Gaman project."""

import os
import environ
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environ.Path(__file__) - 3
APPS_DIR = BASE_DIR.path('gaman')

# Enviroments
env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9_bqs58ror+16_4p-05j5#t77s(c#wmh7(&z$xk3oua#l_#1h%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    # 'social_django', 
    # 'oauth2_provider',
    # 'rest_framework_social_oauth2',
    'django_filters',
]

LOCAL_APPS = [
    'gaman.users',
    'gaman.posts',
    'gaman.sponsorships',
    'gaman.sports',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path('templates'))],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social_django.context_processors.backends', 
                # 'social_django.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True

timezone = TIME_ZONE

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth user
AUTH_USER_MODEL = 'users.User'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Facebook OAuth2 (cliend_id and secret)
# SOCIAL_AUTH_FACEBOOK_KEY = config('CLIENT_ID')
# SOCIAL_AUTH_FACEBOOK_SECRET = config('SECRET')

# Except auth Facebook
# SOCIAL_AUTH_RAISE_EXCEPTIONS = False
# LOGIN_ERROR_URL = '/error-facebook/'

# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link'] 

# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {  
#   'fields': 'id, name, email, picture.type(large), link'
# }

# # OAuth2 Facebook backend 
# DRFSO2_PROPRIETARY_BACKEND_NAME = 'Facebook'
# # DRFSO2_URL_NAMESPACE = 'social'

# SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [               
#     ('name', 'name'),
#     ('email', 'email'),
#     ('picture', 'picture'),
#     ('link', 'profile_url'),
# ]

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer', 
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'rest_framework_social_oauth2.authentication.SocialAuthentication'
    ],
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 3,
}

# AUTHENTICATION_BACKENDS = [
#     'social_core.backends.facebook.FacebookAppOAuth2',
#     'social_core.backends.facebook.FacebookOAuth2',
#     'rest_framework_social_oauth2.backends.DjangoOAuth2',
#     'django.contrib.auth.backends.ModelBackend'
# ]

# Celery
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

# Geocodification Api
API_MAPS_URL = 'https://geocode.search.hereapi.com/v1/geocode'
API_MAPS_ID = config('API_MAPS_ID')
API_MAPS_KEY = config('API_MAPS_KEY')