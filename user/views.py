from django.shortcuts import redirect
from rest_auth import views as auth_views
from rest_auth.registration import views as reg_views
from allauth.account.views import SignupView, LoginView, LogoutView
from rest_framework.renderers import TemplateHTMLRenderer

signupView = SignupView()
signupView.template_name = 'signup.html'
loginView = LoginView()
loginView.template_name = 'login.html'
logoutView = LogoutView()
logoutView.template_name = 'logout.html'


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
		view.request = request._request
		return getattr(view, request.method.lower())(request._request, args, kwargs)

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

			signupView.request = request._request
			return signupView.get(request._request, args, kwargs)

		return super(UserView, self).get(request, args, kwargs)

	def post(self, request, *args, **kwargs):
		if BrowserRequest(request):
			signupView.request = request._request
			return signupView.post(request._request)
		return super(UserView, self).post(request, args, kwargs)


class PasswordView(auth_views.PasswordChangeView, auth_views.PasswordResetView, auth_views.PasswordResetConfirmView):
	def post(self, request, *args, **kwargs):
		view = auth_views.PasswordChangeView if request.user.is_authenticated else auth_views.PasswordResetView
		return view.post(self, request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return auth_views.PasswordResetView.post(self, request, *args, **kwargs)
