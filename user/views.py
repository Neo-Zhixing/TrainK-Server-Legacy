from django.shortcuts import redirect
from rest_auth import views as auth_views
from rest_auth.registration import views as reg_views
from allauth.account.views import LoginView, LogoutView, SignupView, ConfirmEmailView
from rest_framework.renderers import TemplateHTMLRenderer

loginView = LoginView.as_view(template_name='login.html')
logoutView = LogoutView.as_view(template_name='logout.html')
signupView = SignupView.as_view(template_name='signup.html')


def BrowserRequest(request):
	# The lack of accepted renderer indicates that the content negotiation failed,
	# in which case the rest framework will always use the first renderer, TemplateHTMLRenderer.
	# That's why we directly return True here.
	if not hasattr(request, 'accepted_renderer'):
		return True
	return isinstance(request.accepted_renderer, TemplateHTMLRenderer)


class SessionView(auth_views.LoginView, auth_views.LogoutView):
	def _request_view(self, request, *args, **kwargs):
		view = logoutView if request.user.is_authenticated else loginView
		return view(request._request, args, kwargs)

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

	def check_permissions(self, request):
		if request.method is 'POST' or request.method is 'GET':
			return
		super(UserView, self).check_permissions

	def get(self, request, *args, **kwargs):
		if BrowserRequest(request):  # Browser Accessing
			if request.user.is_authenticated:
				return redirect('account_settings')

			return signupView(request._request, args, kwargs)

		return super(UserView, self).get(request, args, kwargs)

	def post(self, request, *args, **kwargs):
		if BrowserRequest(request):
			return signupView(request._request)
		return super(UserView, self).post(request, args, kwargs)


class EmailView(ConfirmEmailView):
	template_name = 'email/confirm.html'


class PasswordView(auth_views.PasswordChangeView, auth_views.PasswordResetView, auth_views.PasswordResetConfirmView):
	def post(self, request, *args, **kwargs):
		view = auth_views.PasswordChangeView if request.user.is_authenticated else auth_views.PasswordResetView
		return view.post(self, request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return auth_views.PasswordResetView.post(self, request, *args, **kwargs)
