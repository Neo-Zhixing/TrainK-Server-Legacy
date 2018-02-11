from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from info.views import GetStation
from info.models import Station
from utils.mixins import MethodPermissionMixin
from .managers import DataManager, CRIsAuthenticated
from .serializers import ProfileSerializer


class DataManagerMixin:
	@property
	def manager(self):
		return DataManager(self.request)


class UserView(RetrieveAPIView):
	serializer_class = ProfileSerializer
	permission_classes = (IsAuthenticated,)

	def get_object(self):
		if not hasattr(self.request.user, 'cr_profile'):
			raise NotFound('The user has no 12306 account associated')
		return self.request.user.cr_profile


class UserPassengerView(APIView, DataManagerMixin):
	permission_classes = (CRIsAuthenticated,)

	def get(self, request):
		data = self.manager.userContacts()
		return Response(data)


def CaptchaView(request):
	manager = DataManager(request)
	return HttpResponse(manager.get_login_captcha(), content_type="image/jpeg")


class SessionView(APIView, DataManagerMixin):
	def get(self, request):
		self.manager.check_session_status()
		return Response(None, status=status.HTTP_204_NO_CONTENT)

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


class TicketView(MethodPermissionMixin, APIView, DataManagerMixin):
	method_permission_classes = {
		'POST': (CRIsAuthenticated, )
	}

	@never_cache
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
		self.manager.placeOrder(request.data, Station.objects)
		return Response(None, status.HTTP_204_NO_CONTENT)


class OrderView(APIView, DataManagerMixin):
	permission_classes = (IsAuthenticated, )
	passenger_name_map = {
		'address': True,
		'born_date': 'birthday',
		'country_code': 'nationality',
		'email': True,
		'mobile_no': 'phone',
		'passenger_id_no': 'certificate',
		'passenger_id_type_code': 'certificateType',
		'passenger_name': 'name',
		'passenger_type': 'type',
		'postalcode': 'zipcode',
		'sex_code': 'gender'
	}

	ticket_name_map = {
		'train_no': ('trainTelecode', None),
		'station_train_code': ('trainName', None),
		'lishi': ('duration', None),
		'start_time': ('departureTime', lambda x: x[0:2] + ':' + x[2:4]),
		'arrive_time': ('arrivalTime', lambda x: x[0:2] + ':' + x[2:4]),
		'from_station_name': ('departureStation', None),
		'to_station_name': ('arrivalStation', None),
	}

	def get(self, request):
		response = self.manager.orderInfo()
		if not response['code'] == 0:
			raise NotFound()
		passengers = response['passengers']['normal_passengers']
		newPassengers = []
		for passenger in passengers:
			newPassenger = {}
			for key, handler in self.passenger_name_map.items():
				if handler is True:
					newPassenger[key] = passenger[key]
				elif isinstance(handler, str):
					newPassenger[handler] = passenger[key]
			newPassengers.append(newPassenger)
		response['passengers'] = newPassengers

		response['certMap'] = {}
		for cert in response['info']['cardTypes']:
			response['certMap'][cert['id']] = cert['value']

		response['ticketTypeMap'] = {}
		for ticketType in response['info']['limitBuySeatTicketDTO']['ticket_type_codes']:
			response['ticketTypeMap'][ticketType['id']] = ticketType['value']

		response['availableSeats'] = []
		for seat in response['info']['limitBuySeatTicketDTO']['seat_type_codes']:
			response['availableSeats'].append(seat['id'])

		response['ticket'] = {}
		for key, (convertedKey, handler) in self.ticket_name_map.items():
			value = response['info']['queryLeftNewDetailDTO'][key]
			if handler:
				value = handler(value)
			response['ticket'][convertedKey] = value

		return Response(response)

	def put(self, request):
		return Response(self.manager.preconfirmOrder(request.data))

	def post(self, request):
		data = self.manager.confirmOrder(request.data)
		return Response(data)

	def patch(self, request):
		data = self.manager.queue()
		return Response(data['data'])
