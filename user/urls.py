from importlib import import_module
from django.urls import path, include
from django.views.generic import TemplateView
from .views import session, user
from allauth import app_settings
from allauth.socialaccount import providers

urlpatterns = [
	path('', user.UserView.as_view(), name='account_signup'),
	path('password/', TemplateView.as_view(), name='account_reset_password'),
	path('session/', session.SessionView.as_view(), name='account_login'),
	path('session/', session.SessionView.as_view(), name='account_logout'),
]


if app_settings.SOCIALACCOUNT_ENABLED:
	urlpatterns += [path('social/', include('allauth.socialaccount.urls'))]

for provider in providers.registry.get_list():
	try:
		prov_mod = import_module(provider.get_package() + '.urls')
	except ImportError:
		continue
	prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
	if prov_urlpatterns:
		urlpatterns += prov_urlpatterns
