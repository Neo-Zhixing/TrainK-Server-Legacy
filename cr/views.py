from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from info.views import GetStation
from info.models import Station
from .managers import DataManager
from .serializers import ProfileSerializer


class DataManagerMixin:
	@property
	def manager(self):
		return DataManager(self.request)


class UserView(RetrieveAPIView):
	serializer_class = ProfileSerializer

	def get_object(self):
		if not hasattr(self.request.user, 'cr_profile'):
			raise NotFound('The user has no 12306 account associated')
		return self.request.user.cr_profile


def CaptchaView(request):
	manager = DataManager(request)
	return StreamingHttpResponse(manager.get_login_captcha_stream(), content_type="image/jpeg")


class SessionView(APIView, DataManagerMixin):
	def convert_result(self, result):
		if 'result_message' in result:
			result['detail'] = result.pop('result_message')
		if 'result_code' in result:
			result['code'] = int(result.pop('result_code'))
		result.pop('apptk', None)
		result.pop('newapptk', None)
		return result

	def get(self, request):
		if hasattr(request.user, 'cr_profile'):
			status = self.convert_result(self.manager.check_session_status())
			code = 0 if status['data']['flag'] else 1
		else:
			code = 2
		return Response({
			'code': code,
			'message': ['Logged in', 'Unauthenticated', 'No associated 12306 account'][code]
		})

		return Response(status)

	def post(self, request):
		data = request.data
		assert 'captcha' in data and data['captcha'], \
			ParseError('Field captcha is required')
		captcha = data.pop('captcha')

		update = hasattr(request.user, 'cr_profile')
		serializer = ProfileSerializer(request.user.cr_profile, data=data, context={'request': request}, partial=True) \
			if update else ProfileSerializer(data=data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		data = serializer.validated_data

		assert {'username', 'password'} <= set(data.keys()) or update, \
			ParseError('Request Incomplete')
		result = self.manager.login(
			username=data['username'] if 'username' in data else request.user.cr_profile.username,
			password=data['password'] if 'password' in data else request.user.cr_profile.password,
			captcha=captcha
		)
		result = self.convert_result(result)

		if result['code'] == 0:
			serializer.save()

		status_codes = [
			status.HTTP_202_ACCEPTED,     # Success
			status.HTTP_403_FORBIDDEN,    # Password/Email/Phone Wrong
			status.HTTP_403_FORBIDDEN,    # Unknown
			status.HTTP_403_FORBIDDEN,    # Unknown
			status.HTTP_403_FORBIDDEN,    # Captcha Success
			status.HTTP_403_FORBIDDEN,    # Captcha Failed
			status.HTTP_403_FORBIDDEN,    # Unknown
			status.HTTP_410_GONE,         # Captcha Outdated
			status.HTTP_502_BAD_GATEWAY,  # Upstream Refused
		]
		return Response(result, status=status_codes[result['code']])


class TicketView(APIView, DataManagerMixin):
	def get(self, request):
		assert {'date', 'from', 'to'} <= set(request.GET), \
			ParseError('Request Params Incomplete')
		from_station = GetStation(request.GET['from'])
		to_station = GetStation(request.GET['to'])
		result = self.manager.tickets(
			from_station=from_station,
			to_station=to_station,
			date=request.GET['date']
		)
		status_codes = [status.HTTP_200_OK, status.HTTP_502_BAD_GATEWAY]

		return Response(result, status=status_codes[result['code']])

	def post(self, request):
		response = self.manager.placeOrder(request.data, Station.objects)
		return Response(response)
