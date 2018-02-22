import os
from .utils import *
from .base import *
DEBUG = True

ALLOWED_HOSTS.append('home.zhangzhixing.cn')
ALLOWED_HOSTS.append('192.168.1.10')

CACHES['default'] = {
	'BACKEND': 'redis_cache.RedisCache',
	'LOCATION': 'localhost:6379',
	'OPTIONS': {
		'DB': 0,
		'PASSWORD': 'Braungardt4365',
	},
}

DATABASES['default'] = {
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'NAME': 'TrainK',
	'USER': 'TrainK',
	'PASSWORD': 'Braungardt4365',
	'HOST': 'localhost',
	'PORT': '5432',
}

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = 'redis://:Braungardt4365@localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://:Braungardt4365@localhost:6379/2'

WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = os.path.join(BASE_DIR, 'build/webpack-stats.prod.json')

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?localhost:?\d*$', )
