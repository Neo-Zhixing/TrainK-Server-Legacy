import requests
import re
import json
from datetime import date


def ticketType(value):
	if value == '有':
		return True
	if value == '无':
		return False
	if value == '':
		return None
	return int(value)


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
		('A6', ticketType),
		('MIN', ticketType),
		('A4', ticketType),
		('A2', ticketType),
		('P', ticketType),
		('WZ', ticketType),
		('yb_num', ticketType),
		('A3', ticketType),
		('A1', ticketType),
		('O', ticketType),
		('M', ticketType),
		('A9', ticketType),
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


def ParseTicketStr(ticket_str, date):
	values = ticket_str.split('|')
	result = _parse(values)
	result['date'] = date
	return result


def _redirect_response(response):
	return response.status_code in {requests.codes.found, requests.codes.moved}


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
			print("Headers:" + str(response.request.headers))
			print("Cookies:" + str(self.session.cookies))
			print("-----------------------------------------")
			print("Received Response: " + ('Streamed Data' if kwargs['stream'] else response.text[0:100] + '...'))
			print("Cookies:" + str(response.cookies))
			print("-----------------------------------------")
			cookieJar = requests.utils.dict_from_cookiejar(self.session.cookies)
			cookieJar.update(requests.utils.dict_from_cookiejar(response.cookies))
			self.request.session[self.cookie_name] = cookieJar
		self.session.hooks['response'].append(ResponseHandler)

		# Fetch Cookie
		if not {'JSESSIONID', 'route', 'BIGipServerotn'} <= set(self.session.cookies.keys()):
			self.session.head('https://kyfw.12306.cn/otn/login/init')

	captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'

	def get_login_captcha_stream(self):
		response = self.session.get(self.captcha_url, stream=True)

		def url2yield():
			chunk = True
			while chunk:
				chunk = response.raw.read(128)
				if not chunk:
					break
				yield chunk
		return url2yield()

	captcha_check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
	login_url = 'https://kyfw.12306.cn/passport/web/login'
	auth_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
	login_complete_url = 'https://kyfw.12306.cn/otn/uamauthclient'

	def auth(self):
		response = self.session.post(self.auth_url, data={'appid': 'otn'})
		return response.json()

	def login(self, username, password, captcha):
		response = self.session.post(self.captcha_check_url, {
			'answer': captcha,
			'login_site': 'E',
			'rand': 'sjrand'
		}).json()

		if int(response['result_code']) != 4:  # Captcha check success when 'result_code' is 4
			return response

		response = self.session.post(self.login_url, data={
			'username': username,
			'password': password,
			'appid': 'otn'
		}, allow_redirects=False)
		if response.status_code == requests.codes.moved or response.status_code == requests.codes.found:
			return {
				'code': 8,
				'detail': 'upstream server refused the connection.'
			}
		response = response.json()
		if int(response['result_code']) != 0:
			return response

		response = self.session.post('https://kyfw.12306.cn/otn/login/userLogin')

		response = self.auth()
		if int(response['result_code']) != 0:
			return response

		response = self.session.post(self.login_complete_url, data={'tk': response['newapptk']})

		return response.json()

	ticket_query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'

	def tickets(self, from_station, to_station, date):
		response = self.session.get(self.ticket_query_url, allow_redirects=False, params={
			'leftTicketDTO.train_date': date,
			'leftTicketDTO.from_station': from_station.telecode,
			'leftTicketDTO.to_station': to_station.telecode,
			'purpose_codes': 'ADULT'
		})
		if response.status_code == requests.codes.moved or response.status_code == requests.codes.found:
			return {
				'code': 1,
				'detail': 'upstream server refused the connection.'
			}
		response = response.json()['data']

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
		response = self.session.get(self.user_check_url).json()
		return response

	def placeOrder(self, ticket, queryset):
		response = self.check_session_status()
		if not response['data']['flag']:
			return {
				'code': 1,
				'detail': 'CR Login Required'
			}
		response = self.session.post(self.order_url, data={
			'secretStr': requests.utils.unquote(ticket['secret']),
			'train_date': ticket['date'],
			'back_train_date': date.today().isoformat(),
			'tour_flag': 'dc',  # dc 单程
			'purpose_codes': 'ADULT',  # adult 成人票
			'query_from_station_name': queryset.get(telecode=ticket['departureStation']).name,
			'query_to_station_name': queryset.get(telecode=ticket['arrivalStation']).name
		}, allow_redirects=False)
		if _redirect_response(response):
			return {'code': 1}
		response = response.json()
		if not response['status']:  # 可能是secret过期。这里需要确认。
			response['code'] = 2
			return response
		return {'code': 0}

	def orderInfo(self):
		response = self.session.post(self.order_token_url, allow_redirects=False)
		if _redirect_response(response):
			return {
				'code': 1,
				'details': 'No Order Info'
			}
		response = response.text
		submit_token = re.search(r"var globalRepeatSubmitToken = '(\S+)'", response).group(1)
		passenger = re.search(r'var ticketInfoForPassengerForm=(\{.+\})?', response).group(1)
		passenger = json.loads(passenger.replace("'", '"'))
		order_request = re.search(r'var orderRequestDTO=(\{.+\})?', response).group(1)
		order_request = json.loads(order_request.replace("'", '"'))
		result = {
			'code': 0,
			'token': submit_token,
			'passenger': passenger,
			'order': order_request
		}

		response = self.session.post(self.passenger_info_url, data={
			'REPEAT_SUBMIT_TOKEN': submit_token
		}).json()
		if response['status']:
			result['passengers'] = response['data']

		return result
