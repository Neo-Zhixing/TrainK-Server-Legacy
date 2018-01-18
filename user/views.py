from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from rest_auth import views as auth_views
from rest_auth.registration import views as reg_views
from allauth.account import views
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from .serializers import EmailSerializer

loginView = views.LoginView.as_view(template_name='login.html')
logoutView = views.LogoutView.as_view(template_name='logout.html')
signupView = views.SignupView.as_view(template_name='signup.html')
passwordChangeView = views.PasswordChangeView.as_view()
passwordSetView = views.PasswordSetView.as_view()
passwordResetView = views.PasswordResetView.as_view(template_name='password/reset.html')
emailManagementView = views.EmailView.as_view(template_name='email/manage.html')


def BrowserRequest(request):
	# The lack of accepted renderer indicates that the content negotiation failed,
	# in which case the rest framework will always use the first renderer, TemplateHTMLRenderer.
	# That's why we directly return True here.
	print(request)
	if not hasattr(request, 'accepted_renderer'):
		return True
	return isinstance(request.accepted_renderer, TemplateHTMLRenderer)


class SessionView(auth_views.LoginView, auth_views.LogoutView):
	@never_cache
	def dispatch(self, *args, **kwargs):
		return super(EmailViewSet, self).dispatch(*args, **kwargs)

	def _request_view(self, request, *args, **kwargs):
		view = logoutView if request.user.is_authenticated else loginView
		return view(request._request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		if BrowserRequest(request):
			return self._request_view(request)
		# TODO: Session Info JSON Return.

	# Logging in.
	def post(self, request, *args, **kwargs):
		if BrowserRequest(request):
			return self._request_view(request)
		return auth_views.LoginView.post(self, request, args, kwargs)

	# Refresh session info.
	# Basically log you out and then relog you in using the request info you provided.
	def put(self, request, *args, **kwargs):
		auth_views.LogoutView.post(self, request, args, kwargs)
		return auth_views.LoginView.post(self, request, args, kwargs)

	# Logging out
	def delete(self, request, *args, **kwargs):
		return auth_views.LogoutView.post(self, request, args, kwargs)


class UserView(auth_views.UserDetailsView, reg_views.RegisterView):
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
		return super(EmailViewSet, self).dispatch(*args, **kwargs)

	def check_permissions(self, request):
		if request.method is 'POST' or request.method is 'GET':
			return
		super(UserView, self).check_permissions

	def get(self, request, *args, **kwargs):
		if BrowserRequest(request):  # Browser Accessing
			if request.user.is_authenticated:
				return redirect('account_settings')

			return signupView(request._request, *args, **kwargs)

		return super(UserView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if BrowserRequest(request):
			return signupView(request._request)
		return super(UserView, self).post(request, *args, **kwargs)


class PasswordView(auth_views.PasswordChangeView, auth_views.PasswordResetView, auth_views.PasswordResetConfirmView):
	@never_cache
	def dispatch(self, *args, **kwargs):
		return super(EmailViewSet, self).dispatch(*args, **kwargs)

	def _browser_view(self, request, *args, **kwargs):
		view = passwordChangeView if request.user.is_authenticated else passwordResetView
		return view(request._request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		return self._browser_view(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if BrowserRequest(request):
			return self._browser_view(request, *args, **kwargs)
		return auth_views.PasswordResetConfirmView.post(self, request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return auth_views.PasswordChangeView.post(self, request, *args, **kwargs)

	def check_permissions(self, request):
		if request.method is 'POST' or request.method is 'GET':
			return
		super(PasswordView, self).check_permissions

	def delete(self, request, *args, **kwargs):
		return auth_views.PasswordResetView.post(self, request, *args, **kwargs)


class EmailViewSet(ModelViewSet):
	template_name = 'email/manage.html'
	serializer_class = EmailSerializer
	pagination_class = None

	@never_cache
	def dispatch(self, *args, **kwargs):
		return super(EmailViewSet, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return self.request.user.emailaddress_set.all()

	def get_object(self):
		return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

	def list(self, request, *args, **kwargs):
		if BrowserRequest(request):
			return emailManagementView(request._request)
		return super(EmailViewSet, self).list(self, request, *args, **kwargs)


class SettingView(APIView):
	template_name = 'settings.html'
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		return Response()
