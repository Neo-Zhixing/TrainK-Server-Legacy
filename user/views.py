from django.shortcuts import reverse, get_object_or_404
from django.views.generic.base import RedirectView
from django.views.decorators.cache import never_cache
from rest_auth import views as auth_views
from rest_auth.registration import views as reg_views
from allauth.account import views
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from utils.mixins import VersatileViewMixin
from .serializers import EmailSerializer


class SessionView(VersatileViewMixin, auth_views.LoginView, auth_views.LogoutView):
	@never_cache
	def dispatch(self, *args, **kwargs):
		return super(SessionView, self).dispatch(*args, **kwargs)

	@property
	def template_view(self):
		return views.LogoutView.as_view(template_name='logout.html') \
			if self.request.user.is_authenticated \
			else views.LoginView.as_view(template_name='login.html')

	# Refresh session info.
	# Basically log you out and then relog you in using the request info you provided.
	def put(self, request, *args, **kwargs):
		auth_views.LogoutView.post(self, request, args, kwargs)
		return auth_views.LoginView.post(self, request, args, kwargs)

	# Logging out
	def delete(self, request, *args, **kwargs):
		return auth_views.LogoutView.post(self, request, args, kwargs)


class UserView(VersatileViewMixin, auth_views.UserDetailsView, reg_views.RegisterView):
	# Browser Requests:
	# Authenticated Users redirect to settings page
	# Anonymous Users get Allauth Signup page
	#
	# API Requests:
	# GET, PUT, PATCH direct to UserDetailsView
	# POST direct to RegisterView
	# Activation for unauthenticated users not implemented. WHERE TO PUT?

	@never_cache
	def dispatch(self, *args, **kwargs):
		return super(UserView, self).dispatch(*args, **kwargs)

	@property
	def template_view(self):
		return RedirectView.as_view(url=reverse('account_settings'), permanent=True) \
			if self.request.user.is_authenticated \
			else views.SignupView.as_view(template_name='signup.html')

	def check_permissions(self, request):
		if request.method is 'POST' or request.method is 'GET':
			return
		super(UserView, self).check_permissions


class PasswordView(VersatileViewMixin, auth_views.PasswordChangeView, auth_views.PasswordResetView, auth_views.PasswordResetConfirmView):
	@never_cache
	def dispatch(self, *args, **kwargs):
		return super(PasswordView, self).dispatch(*args, **kwargs)

	@property
	def template_view(self):
		if not self.request.user.is_authenticated:
			return views.PasswordResetView.as_view(template_name='password/reset.html')
		return views.PasswordChangeView.as_view() \
			if self.request.user.has_usable_password() \
			else views.PasswordSetView.as_view()

	def post(self, request, *args, **kwargs):
		return auth_views.PasswordResetConfirmView.post(self, request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return auth_views.PasswordChangeView.post(self, request, *args, **kwargs)

	def check_permissions(self, request):
		if request.method is 'POST' or request.method is 'GET':
			return
		super(PasswordView, self).check_permissions

	def delete(self, request, *args, **kwargs):
		return auth_views.PasswordResetView.post(self, request, *args, **kwargs)


class EmailViewSet(VersatileViewMixin, ModelViewSet):
	serializer_class = EmailSerializer
	pagination_class = None
	permission_classes = (IsAuthenticated,)
	template_views = {
		'list': views.EmailView.as_view(template_name='email/manage.html')
	}

	@never_cache
	def dispatch(self, *args, **kwargs):
		return super(EmailViewSet, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return self.request.user.emailaddress_set.all()

	def get_object(self):
		return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])


class SettingView(APIView):
	template_name = 'app.html'
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		return Response()
