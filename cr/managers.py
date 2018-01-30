import requests
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
	('buttonText', str),
	('trainTelecode', str),
	('trainName', str),
	('originStation', str),
	('destinationStation', str),
	('departureStation', str),
	('arrivalStation', str),
	('departureTime', str),
	('arrivalTime', str),
	('duration', str),
	('purchasability', lambda x: {'Y': True, 'N': False, 'IS_TIME_NOT_BUY': None}.get(x, None)),
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
		session = requests.Session()
		session.headers = self.default_headers
		session.headers['User-Agent'] = request.META.get('HTTP_USER_AGENT', self.default_user_agent)
		session.cookies = requests.cookies.cookiejar_from_dict(request.session.get(self.cookie_name, {}))

		# Fetch Cookie
		cookieKeys = set(session.cookies.keys())
		if not {'JSSESSIONID', 'route', 'BIGipServerotn'} <= cookieKeys:
			session.head('https://kyfw.12306.cn/otn/login/init')

		self.session = session

	def get_session(self, referer):
		self.session.headers['Referer'] = referer
		return self.session

	def save(self):
		self.request.session[self.cookie_name] = requests.utils.dict_from_cookiejar(self.session.cookies)

	captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'

	def get_login_captcha_stream(self):
		response = self.session.get(self.captcha_url, stream=True)
		self.save()

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
	session_status_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
	login_complete_url = 'https://kyfw.12306.cn/otn/uamauthclient'

	def login(self, username, password, captcha):
		if int(self.check_session_status()['result_code']) == 0:
			return {
				'code': 2,
				'detail': 'Already Logged In'
			}

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

		response = self.session.post(self.session_status_url, data={"appid": "otn"}).json()
		if int(response['result_code']) != 0:
			return response

		self.session.cookies['tk'] = response['newapptk']

		response = requests.post(self.login_complete_url, data={'tk': response['newapptk']}).json()
		self.save()

		return response

	def check_session_status(self):
		response = self.session.get(self.session_status_url, params={"appid": "otn"}).json()
		if 'newapptk' in response:
			self.session.cookies['tk'] = response['newapptk']
		self.save()
		return response

	ticket_query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'

	def tickets(self, from_station, to_station, date):
		response = self.session.get(self.ticket_query_url, allow_redirects=False, params={
			'leftTicketDTO.train_date': date,
			'leftTicketDTO.from_station': from_station.telecode,
			'leftTicketDTO.to_station': to_station.telecode,
			'purpose_codes': 'ADULT'
		})
		self.save()
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

	def placeOrder(self, ticket, queryset):
		response = self.session.post(self.user_check_url).json()
		print(self.session.cookies)
		if not response['data']['flag']:
			return {
				'code': 1,
				'detail': 'CR Login Required'
			}
		response = self.session.post(self.order_url, data={
			'secretStr': ticket['secret'],
			'train_date': ticket['date'],
			'back_train_date': date.today().isoformat(),
			'tour_flag': 'dc',  # dc 单程
			'purpose_codes': 'ADULT',  # adult 成人票
			'query_from_station_name': queryset.get(telecode=ticket['departureStation']).name,
			'query_to_station_name': queryset.get(telecode=ticket['arrivalStation']).name
		})
		print(response.text)
		return response.text
