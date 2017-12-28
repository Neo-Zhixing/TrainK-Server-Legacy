"""
Django settings for TrainK project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from machina import get_apps as get_machina_apps
from machina import MACHINA_MAIN_TEMPLATE_DIR, MACHINA_MAIN_STATIC_DIR

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#hzqu*0-tby7iyvberwew29vv^c_b(*w-zux+f73hcqv9-xf53'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
INTERNAL_IPS = ('127.0.0.1')

ALLOWED_HOSTS = ['tra.ink', 'localhost', '192.168.1.101']
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'webpack_loader',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',

    'user',
    'info',
    'ticket',
    'trip',

    # Machina related apps:
    'mptt',
    'haystack',
    'widget_tweaks',
] + get_machina_apps()

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TrainK.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
            MACHINA_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'machina.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'TrainK.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'TrainK',
        'USER': 'TrainK',
        'PASSWORD': 'Braungardt4365',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


STATIC_URL = '/web/'
STATICFILES_DIRS = (
    MACHINA_MAIN_STATIC_DIR,
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, 'dist'),
)
STATICFILES_STORAGE = 'aliyun_oss2_storage.backends.AliyunStaticStorage'
DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
ACCESS_KEY_ID = "LTAIP3L1SzIaldrp"
ACCESS_KEY_SECRET = "hUf7QPw1TL7tM18QfMw74fpRCSo5G8"
END_POINT = "oss-cn-hangzhou.aliyuncs.com"  # OSS存储节点
BUCKET_NAME = "traink"
ALIYUN_OSS_CNAME = "https://static.tra.ink"
BUCKET_ACL_TYPE = "public-read"  # private, public-read, public-read-write


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.TemplateHTMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
LOGIN_REDIRECT_URL = '/user'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

# Machina
MACHINA_FORUM_NAME = 'TrainK'
MACHINA_BASE_TEMPLATE_NAME = 'base.html'
# Django-haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

_WEBPACK_STAT_FILE_PATH = 'build/webpack-stats.dev.json' if DEBUG else 'build/webpack-stats.prod.json'
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, _WEBPACK_STAT_FILE_PATH),
    }
}
