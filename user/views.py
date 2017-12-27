from rest_auth import views as auth_views
from rest_auth.registration import views as reg_views


class SessionView(auth_views.LoginView, auth_views.LogoutView):
	# POST direct to LoginView
	def delete(self, request, *args, **kwargs):
		return auth_views.LogoutView.post(self, request, args, kwargs)


class UserView(auth_views.UserDetailsView, reg_views.RegisterView):
	# GET, PUT, PATCH direct to UserDetailsView
	# POST direct to RegisterView
	# Activation for unauthenticated users not implemented. WHERE TO PUT?
	pass


class PasswordView(auth_views.PasswordChangeView, auth_views.PasswordResetView, auth_views.PasswordResetConfirmView):
	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return auth_views.PasswordChangeView.post(self, request, *args, **kwargs)
		else:
			return auth_views.PasswordResetConfirmView.post(self, request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return auth_views.PasswordResetView.post(self, request, *args, **kwargs)
