import requests
import re
import json
import time
from django.http import StreamingHttpResponse
from rest_framework.exceptions import ParseError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from info.views import GetStation
from .exceptions import UpstreamRefused


def session_method(method):
	def wrapper(self, request, *args, **kwargs):
		session = requests.Session()
		session.headers = {
			'Host': 'kyfw.12306.cn',
			'Origin': 'https://kyfw.12306.cn',
			'X-Requested-With': 'XMLHttpRequest',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Referer': 'https://kyfw.12306.cn/otn/login/init',
			'Accept': '*/*',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'User-Agent': request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'),
		}
		session.cookies = requests.cookies.cookiejar_from_dict(request.session.get('CRCookies', {}))

		timestamp = int(time.time() * 1000)
		# Fetch Cookie
		cookieKeys = set(session.cookies.keys())
		if not {'JSSESSIONID', 'route', 'BIGipServerotn'} <= cookieKeys:
			session.head('https://kyfw.12306.cn/otn/login/init')
		if not {'RAIL_EXPIRATION', 'RAIL_DEVICEID'} <= cookieKeys \
			or int(session.cookies['RAIL_EXPIRATION']) - timestamp < 0:
			response = session.get('https://kyfw.12306.cn/otn/HttpZF/logdevice')
			response = re.search('\(\'(.*?)\'\)', response.text).group(1)
			response = json.loads(response)
			session.cookies['RAIL_EXPIRATION'] = response['exp']
			session.cookies['RAIL_DEVICEID'] = response['dfp']

		response = method(self, request, session, *args, **kwargs)
		request.session['CRCookies'] = requests.utils.dict_from_cookiejar(session.cookies)
		return response
	return wrapper


class LoginView(APIView):
	@session_method
	def get(self, request, session):
		response = session.get('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand', stream=True)

		def url2yield():
			chunk = True
			while chunk:
				chunk = response.raw.read(128)
				if not chunk:
					break
				yield chunk
		return StreamingHttpResponse(url2yield(), content_type="image/jpeg")

	@session_method
	def post(self, request, session):
		if 'username' not in request.data or 'password' not in request.data or 'captcha' not in request.data:
			raise ParseError('Request Params Incomplete')

		response = session.post('https://kyfw.12306.cn/passport/captcha/captcha-check', {
			'answer': request.data['captcha'],
			'login_site': 'E',
			'rand': 'sjrand'
		}).json()

		if int(response['result_code']) != 4:  # Captcha check success when 'result_code' is 4
			return Response(response, status=status.HTTP_400_BAD_REQUEST)

		print(session.cookies)
		print(session.headers)
		response = session.post('https://kyfw.12306.cn/passport/web/login', data={
			'username': request.data['username'],
			'password': request.data['password'],
			'appid': 'otn'
		}, allow_redirects=False)
		if response.status_code == requests.codes.moved or response.status_code == requests.codes.found:
			raise UpstreamRefused()
		response = response.json()
		if int(response['result_code']) != 0:
			return Response(response, status=status.HTTP_400_BAD_REQUEST)

		response = session.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data={"appid": "otn"}).json()
		if int(response['result_code']) != 0:
			return Response(response, status=status.HTTP_400_BAD_REQUEST)

		appID = response['newapptk']
		request.session['CRAppID'] = appID

		response = requests.post('https://kyfw.12306.cn/otn/uamauthclient', data={'tk': appID}).json()

		return Response(response)


@api_view(['GET'])
def TicketListView(request):
	if 'date' not in request.GET or 'from' not in request.GET or 'to' not in request.GET:
		raise ParseError('Request Params Incomplete')
	from_station = GetStation(request.GET['from'])
	to_station = GetStation(request.GET['to'])
	session = requests.session()
	print(session.headers)
	response = session.get('https://kyfw.12306.cn/otn/leftTicket/queryZ', allow_redirects=False, params={
		'leftTicketDTO.train_date': request.GET['date'],
		'leftTicketDTO.from_station': from_station.telecode,
		'leftTicketDTO.to_station': to_station.telecode,
		'purpose_codes': 'ADULT'
	})
	print(response.url)
	print(response.text)
	if response.status_code == requests.codes.moved or response.status_code == requests.codes.found:
		raise UpstreamRefused()
	return Response(response.json())
