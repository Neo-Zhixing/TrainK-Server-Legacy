import requests
import re
import json
import time
from datetime import date

from . import exceptions
from rest_framework.exceptions import AuthenticationFailed


def ticketType(value):
	if value == '有':
		return True
	if value == '无':
		return False
	if value == '':
		return None
	if value.isnumeric():
		return int(value)
	return value


keyMap = [
	('secret', str),
	('buttonText', lambda x: None),
	('trainTelecode', str),
	('trainName', str),
	('originStation', str),
	('destinationStation', str),
	('departureStation', str),
	('arrivalStation', str),
	('departureTime', str),
	('arrivalTime', str),
	('duration', str),
	('purchasability', lambda x: {'Y': 0, 'N': 1, 'IS_TIME_NOT_BUY': 2}.get(x, x)),
	('yp_info', str),
	('departureDate', lambda x: '%s-%s-%s' % (x[0:4], x[4:6], x[6:8])),
	('train_seat_feature', str),
	('locationCode', str),

	('departureIndex', int),
	('arrivalIndex', int),
	('IDCardSupported', lambda x: x == '1'),
	('status', int),
	('seats', [
		('gg_num', ticketType),
		('6', ticketType),
		('MIN', ticketType),
		('4', ticketType),
		('2', ticketType),
		('P', ticketType),
		('WZ', ticketType),
		('yb_num', ticketType),
		('3', ticketType),
		('1', ticketType),
		('O', ticketType),
		('M', ticketType),
		('9', ticketType),
		('F', ticketType)
	]),
	('yp_ex', str),
	('seat_types', str),
	('reward', lambda x: x == '1'),
]


def _parse(values, currentKeyMap=keyMap):
	parsedValue = {}
	for key, handler in currentKeyMap:
		if isinstance(handler, list):
			parsedValue[key] = _parse(values, handler)
		else:
			value = handler(values.pop(0))
			if value is not None:
				parsedValue[key] = value
	return parsedValue


class DataManager:
	cookie_name = 'CRCookies'
	default_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
	default_headers = {
		'Host': 'kyfw.12306.cn',
		'Origin': 'https://kyfw.12306.cn',
		'X-Requested-With': 'XMLHttpRequest',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Referer': 'https://kyfw.12306.cn/otn/login/init',
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.8'
	}

	def __init__(self, request):
		self.request = request
		self.session = requests.Session()
		self.session.headers = self.default_headers
		self.session.headers['User-Agent'] = request.META.get('HTTP_USER_AGENT', self.default_user_agent)
		self.session.cookies = requests.cookies.cookiejar_from_dict(request.session.get(self.cookie_name, {}))

		def ResponseHandler(response, *args, **kwargs):
			print("\n\n")
			print("-----------------------------------------")
			print("Sending Request: " + response.request.url)
			print("Sending:" + str(response.request.body))
			print("Headers:" + str(response.request.headers))
			print("Cookies:" + str(self.session.cookies))
			print("-----------------------------------------")
			print("Received Response: " + ('Streamed Data' if kwargs['stream'] else response.text[0:100] + '...'))
			print("Cookies:" + str(response.cookies))
			print("-----------------------------------------")
			if response.is_redirect and response.request.method != 'HEAD':
				raise exceptions.UpstreamRefused()
			cookieJar = requests.utils.dict_from_cookiejar(self.session.cookies)
			cookieJar.update(requests.utils.dict_from_cookiejar(response.cookies))
			self.request.session[self.cookie_name] = cookieJar
		self.session.hooks['response'].append(ResponseHandler)

		# Fetch Cookie
		if not {'JSESSIONID', 'route', 'BIGipServerotn'} <= set(self.session.cookies.keys()):
			self.session.head('https://kyfw.12306.cn/otn/login/init')

	captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'

	def get_login_captcha(self):
		response = self.session.get(self.captcha_url, stream=True)
		return response.content

	captcha_check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
	login_url = 'https://kyfw.12306.cn/passport/web/login'
	auth_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
	login_complete_url = 'https://kyfw.12306.cn/otn/uamauthclient'

	def login(self, username, password, captcha):
		def checkResponse(response, success_code=0):
			if int(response['result_code']) != success_code:
				raise AuthenticationFailed(response['result_message'])

		response = self.session.post(self.captcha_check_url, {
			'answer': captcha,
			'login_site': 'E',
			'rand': 'sjrand'
		}).json()
		checkResponse(response, 4)

		response = self.session.post(self.login_url, data={
			'username': username,
			'password': password,
			'appid': 'otn'
		}, allow_redirects=False).json()
		checkResponse(response)

		response = self.session.head('https://kyfw.12306.cn/otn/login/userLogin')

		response = self.session.post(self.auth_url, data={'appid': 'otn'}).json()
		checkResponse(response)

		response = self.session.post(self.login_complete_url, data={'tk': response['newapptk']}).json()
		checkResponse(response)
		del response['result_message']
		del response['result_code']
		return response

	ticket_query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'

	def tickets(self, from_station, to_station, date):
		response = self.session.get(self.ticket_query_url, allow_redirects=False, params={
			'leftTicketDTO.train_date': date,
			'leftTicketDTO.from_station': from_station.telecode,
			'leftTicketDTO.to_station': to_station.telecode,
			'purpose_codes': 'ADULT'
		})
		try:
			response = response.json()['data']
		except json.decoder.JSONDecodeError:
			raise exceptions.UpstreamDataError

		def ParseTicketStr(ticket_str, date):
			values = ticket_str.split('|')
			result = _parse(values)
			result['date'] = date
			return result
		results = [ParseTicketStr(ticketStr, date) for ticketStr in response['result']]
		return {
			'code': 0,
			'detail': 'Success',
			'results': results,
			'nameMap': response['map']
		}

	user_check_url = 'https://kyfw.12306.cn/otn/login/checkUser'
	order_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
	order_token_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
	passenger_info_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'

	def check_session_status(self):
		if not hasattr(self.request.user, 'cr_profile'):
			return False
		response = self.session.get(self.user_check_url).json()
		return response['data']['flag']

	def placeOrder(self, ticket, queryset):
		response = self.session.post(self.order_url, data={
			'secretStr': requests.utils.unquote(ticket['secret']),
			'train_date': ticket['date'],
			'back_train_date': date.today().isoformat(),
			'tour_flag': 'dc',  # dc 单程
			'purpose_codes': 'ADULT',  # adult 成人票
			'query_from_station_name': queryset.get(telecode=ticket['departureStation']).name,
			'query_to_station_name': queryset.get(telecode=ticket['arrivalStation']).name
		}, allow_redirects=False)
		response = response.json()
		if not response['status']:
			if response['messages'][0] == '您还有未处理的订单，请您到<a href="../queryOrder/initNoComplete">[未完成订单]</a>进行处理!':
				raise exceptions.UnhandledOrder()
			else:
				raise exceptions.CredentialOutdated()
		self.request.session['CRTicket'] = ticket

	def orderInfo(self):
		response = self.session.post(self.order_token_url, allow_redirects=False)
		response = response.text
		submit_token = re.search(r"var globalRepeatSubmitToken = '(\S+)'", response)
		info = re.search(r'var ticketInfoForPassengerForm=(\{.+\})?', response)
		if not (submit_token and info):
			raise exceptions.UpstreamDataError
		submit_token = submit_token.group(1)
		info = json.loads(info.group(1).replace("'", '"'))
		result = {
			'code': 0,
			'token': submit_token,
			'info': info
		}
		self.request.session['CRSubmitInfo'] = {
			'locationCode': result['info']['train_location'],
			'ticketKeyChange': result['info']['key_check_isChange'],
			'leftTicketStr': result['info']['leftTicketStr'],
			'submitToken': submit_token,
			'info': result['info']['queryLeftNewDetailDTO']
		}

		response = self.session.post(self.passenger_info_url, data={
			'REPEAT_SUBMIT_TOKEN': submit_token
		}, allow_redirects=False)
		response = response.json()
		if response['status']:
			result['passengers'] = response['data']

		return result

	order_confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
	order_preconfirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
	queue_info_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
	queue_url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'

	def _get_passenger_str(self, passengers):
		passengerStr = []
		oldPassengerStr = []
		for p in passengers:
			for key, value in p.items():
				p[key] = str(value)
			passengerStr.append(','.join([
				p['selectedSeat'],
				p['selectedTicketType'],
				p['type'],
				p['name'],
				p['certificateType'],
				p['certificate'],
				p['phone'],
				'N'
			]))
			oldPassengerStr.append(','.join([
				p['name'],
				p['certificateType'],
				p['certificate'],
				p['type']
			]))
		return {
			'passengerTicketStr': '_'.join(passengerStr),
			'oldPassengerStr': '_'.join(oldPassengerStr) + '_'
		}

	def preconfirmOrder(self, passengers):
		data = {
			'bed_level_order_num': '000000000000000000000000000000',
			'cancel_flag': '2',
			'REPEAT_SUBMIT_TOKEN': self.request.session['CRSubmitInfo']['submitToken'],
			'randCode': '',
			'tour_flag': 'dc',
			'whatsSelect': '1'
		}
		data.update(self._get_passenger_str(passengers))
		response = self.session.post(self.order_preconfirm_url, data, allow_redirects=False)
		info = response.json()

		data = {
			'fromStationTelecode': self.request.session['CRSubmitInfo']['info']['from_station_telecode'],
			'toStationTelecode': self.request.session['CRSubmitInfo']['info']['to_station_telecode'],
			'station_train_code': self.request.session['CRSubmitInfo']['info']['station_train_code'],
			'leftTicket': self.request.session['CRSubmitInfo']['leftTicketStr'],
			'purpose_codes': '00',
			'REPEAT_SUBMIT_TOKEN': self.request.session['CRSubmitInfo']['submitToken'],
			'seatType': passengers[0]['selectedSeat'],
			'train_date': time.strftime('%a %b %d %Y %H:%M:%S  GMT+0800', time.strptime(self.request.session['CRTicket']['date'], '%Y-%m-%d')),
			'train_location': self.request.session['CRSubmitInfo']['locationCode'],
			'train_no': self.request.session['CRSubmitInfo']['info']['train_no']
		}
		response = self.session.post(self.queue_info_url, data=data, allow_redirects=False)
		queue = response.json()
		if 'data' not in queue:
			raise exceptions.UpstreamDataError(queue['messages'])
		if 'data' not in info:
			raise exceptions.UpstreamDataError(data['messages'])

		return {
			'queue': queue['data'],
			'data': info['data']
		}

	def confirmOrder(self, passengers, seats):
		data = {
			'REPEAT_SUBMIT_TOKEN': self.request.session['CRSubmitInfo']['submitToken'],
			'choose_seats': seats,
			'dwAll': 'N',
			'key_check_isChange': self.request.session['CRSubmitInfo']['ticketKeyChange'],
			'leftTicketStr': self.request.session['CRSubmitInfo']['leftTicketStr'],
			'purpose_codes': '00',
			'randCode': '',
			'roomType': '00',
			'seatDetailType': '000',
			'train_location': self.request.session['CRSubmitInfo']['locationCode'],
			'whatsSelect': '1'
		}
		data.update(self._get_passenger_str(passengers))
		response = self.session.post(self.order_confirm_url, data, allow_redirects=False)
		response = response.json()
		if not response['data']['submitStatus']:
			return response['data']['errMsg']
		return response

	def queue(self):
		response = self.session.get(self.queue_url, params={
			'random': str(round(time.time() * 1000)),
			'tourFlag': 'dc',
			'_json_att': '',
			'REPEAT_SUBMIT_TOKEN': self.request.session['CRSubmitInfo']['submitToken'],
		})
		return response.json()

	# 以下为用户面板有关方法
	# 用户面板/常用联系人
	user_contact_url = 'https://kyfw.12306.cn/otn/passengers/init'

	def userContacts(self):
		response = self.session.get(self.user_contact_url).text
		passengers = re.search(r'var passengers=(\[.+\]);', response)
		if not passengers:
			raise exceptions.UpstreamDataError
		passengers = passengers.group(1).replace("'", '"')
		print(passengers)
		try:
			passengers = json.loads(passengers)
		except json.decoder.JSONDecodeError:
			raise exceptions.UpstreamDataError('Upstream server returned corrupted JSON data.')
		return passengers
