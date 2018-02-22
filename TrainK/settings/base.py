from .utils import *
MODE = Mode.Testing
SECRET_KEY = '#hzqu*0-tby7iyvberwew29vv^c_b(*w-zux+f73hcqv9-xf53'

SITE_ID = 1

ALLOWED_HOSTS = [
	'tra.ink',
	'localhost'
]

INSTALLED_APPS = [
	'baton',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',

	'django_celery_beat',

	'webpack_loader',
	'rest_framework',
	'rest_framework.authtoken',
	'rest_auth',
	'rest_auth.registration',
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'crispy_forms',

	'user',
	'info',
	'ticket',
	'trip',
	'map',
	'scrape',
	'utils',
	'cr',

	'baton.autodiscover',
]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'TrainK.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, "templates"),
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'TrainK.settings.context_processors.mode'
				],
		},
	},
]

WSGI_APPLICATION = 'TrainK.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {}

DEFAULT_FROM_EMAIL = 'TrainK <notification@robot.tra.ink>'
SERVER_EMAIL = 'TrainK <notification@robot.tra.ink>'

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
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

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CACHES = {}

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'dist'),
	os.path.join(BASE_DIR, 'static')
)

CELERY_WORKER_REDIRECT_STDOUTS = False
CELERY_ENABLE_UTC = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

BATON = {
	'SITE_HEADER': 'TrainK Admin',
	'SITE_TITLE': 'TrainK',
	'INDEX_TITLE': 'Site administration',
	'SUPPORT_HREF': '',
	'COPYRIGHT': 'Copyright © 2017 <a href="//begin.studio">begin Studio</a>', # noqa
	'POWERED_BY': '<a href="https://www.otto.to.it">Otto srl</a>',
	'MENU': (
		{'type': 'title', 'label': 'Basic', 'apps': ('sites', )},
		{'type': 'model', 'label': 'Sites', 'name': 'site', 'app': 'sites'},
		{'type': 'app', 'name': 'django_celery_beat', 'label': 'Periodic Tasks', 'icon': 'fa fa-lock'},

		{'type': 'title', 'label': 'Users', 'apps': ('auth', )},
		{'type': 'app', 'name': 'auth', 'label': 'Authentication', 'icon': 'fa fa-lock'},
		{'type': 'model', 'label': 'Tokens', 'name': 'token', 'app': 'authtoken', 'icon': 'fa fa-envelope'},
		{'type': 'app', 'name': 'socialaccount', 'label': 'Social Auth', 'icon': 'fa fa-weibo'},
		{'type': 'model', 'label': 'Emails', 'name': 'emailaddress', 'app': 'account', 'icon': 'fa fa-envelope'},

		{'type': 'title', 'label': 'Info', 'apps': ('info', )},
		{'type': 'app', 'name': 'info', 'label': 'Train Info', 'icon': 'fa fa-info'},
		{'type': 'free', 'label': 'Custom Link', 'url': '/admin/tasks'},
	),
}


REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.TemplateHTMLRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
		'rest_framework.renderers.AdminRenderer',
		'rest_framework.renderers.JSONRenderer',
	),
	'DEFAULT_THROTTLE_CLASSES': (
		'rest_framework.throttling.AnonRateThrottle',
		'rest_framework.throttling.UserRateThrottle'
	),
	'DEFAULT_THROTTLE_RATES': {
		'anon': '10/minute',
		'user': '30/minute'
	},
	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
	'PAGE_SIZE': 20,
	'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
}
OLD_PASSWORD_FIELD_ENABLED = True
LOGIN_REDIRECT_URL = '/user/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SIGNUP_FORM_CLASS = 'user.forms.SignupForm'
ACCOUNT_FORMS = {
	'login': 'user.forms.LoginForm'
}
REST_AUTH_SERIALIZERS = {
	'USER_DETAILS_SERIALIZER': 'user.serializers.UserDetailsSerializer'
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = MODE == Mode.Production

WEBPACK_LOADER = {
	'DEFAULT': {
		'BUNDLE_DIR_NAME': 'dist/',
	}
}
