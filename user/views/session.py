from rest_auth.views import LoginView, LogoutView


class SessionView(LoginView, LogoutView):
	def post(self, request, *args, **kwargs):
		return LoginView.post(self, request, args, kwargs)

	def delete(self, request, *args, **kwargs):
		return LogoutView.post(self, request, args, kwargs)
