from rest_framework.views import APIView

from allauth.account.views import SignupView

signupView = SignupView()
signupView.template_name = 'signup.html'


class UserView(APIView):

	def get(self, request):
		if request.user.is_authenticated:
			return None
		else:
			signupView.request = request._request
			return signupView.get(request._request)

	def post(self, request):
		if request.user.is_authenticated:
			return None
		else:
			signupView.request = request._request
			return signupView.post(request._request)
