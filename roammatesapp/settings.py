"""
Django settings for roammatesapp project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
import environ

env = environ.Env()

# Load environment variables from a .env file if present
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vvj@lnk0f*@we+()pto6n@e7@=+0&i64s1xto5_!n1vin=#^6^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third_party_apps
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'drf_spectacular',
    "corsheaders",
    'django_celery_beat',
    'django_celery_results',
    'multiselectfield',

    # local apps
    'core',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom
    "corsheaders.middleware.CorsMiddleware",
    # 'django_sonar.middlewares.requests.RequestsMiddleware',
]

ROOT_URLCONF = 'roammatesapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

WSGI_APPLICATION = 'roammatesapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Other settings
# DJOSER SETTINGS
DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'current_user': 'users.serializers.CurrentUserSerializer',
    }
}

# CORS HEADERS
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
]

# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # drf-spectacular settings

    # API rate limiting
    'DEFAULT_THROTTLE_CLASSES': [

        'rest_framework.throttling.AnonRateThrottle',

        'rest_framework.throttling.UserRateThrottle'

    ],

    'DEFAULT_THROTTLE_RATES': {

        'anon': '100/day',

        'user': '1000/day'

    },

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
}

AUTH_USER_MODEL = 'core.CustomUser'

# API Docs settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Roammates App API',
    'DESCRIPTION': 'Roammates App project API Documents',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/backend/api/*',
    # 'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAuthenticated'],
    'DISABLE_ERRORS_AND_WARNINGS': True,
    'COMPONENT_SPLIT_REQUEST': True
}

BASE_BACKEND_URL = "http://localhost:8000"

# EMAIL SETTINGS
EMAIL_HOST_USER = env('SENDER_EMAIL')
EMAIL_HOST_PASSWORD = env('SENDER_EMAIL_PASSWORD')
# print(EMAIL_HOST_PASSWORD)


PHONENUMBER_DEFAULT_REGION = "NG"

# flutterwave settings
FLW_SEC_KEY = env('FLW_SEC_KEY')
FLW_PUB_KEY = env('FLW_PUB_KEY')

# Celery settings
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='json'
CELERY_TIMEZONE='Africa/Lagos'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_DEFAULT_QUEUE = 'celery.importexport.default'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Celery beat settings
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BEAT_SCHEDULE = {
    'delete-expired-ads': {
        'task': 'roammatesapp.tasks.delete_expired_ads',
        'schedule': 3600,  # Run every hour
    },
}