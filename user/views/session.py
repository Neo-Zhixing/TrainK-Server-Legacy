from rest_framework.views import APIView

from allauth.account.views import LoginView, LogoutView

loginView = LoginView()
logoutView = LogoutView()

loginView.template_name = 'login.html'
logoutView.template_name = 'logout.html'


class SessionView(APIView):

	def get(self, request):
		if request.user.is_authenticated:
			logoutView.request = request._request
			return logoutView.get(request._request)
		else:
			loginView.request = request._request
			return loginView.get(request._request)

	def post(self, request):
		if request.user.is_authenticated:
			logoutView.request = request._request
			return logoutView.post(request._request)
		else:
			loginView.request = request._request
			return loginView.post(request._request)
