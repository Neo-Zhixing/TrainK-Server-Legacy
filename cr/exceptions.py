from rest_framework.exceptions import APIException
from rest_framework import status


class UpstreamRefused(APIException):
	status_code = status.HTTP_503_SERVICE_UNAVAILABLE
	default_detail = 'Upstream Server (12306.cn) refused the connection.'
	default_code = 'service_unavailable'


class UpstreamDataError(APIException):
	status_code = status.HTTP_503_SERVICE_UNAVAILABLE
	default_detail = 'Upstream Server (12306.cn) returned some unexpected data due to a change in the data transfer protocol.'
	default_code = 'service_unavailable'


class SessionContextMissing(APIException):
	status_code = status.HTTP_400_BAD_REQUEST
	default_detail = 'Upstream Server refused the request for the lack of appropriate session context.'


class CredentialOutdated(APIException):
	status_code = status.HTTP_410_GONE
	default_detail = 'Outdated secret key was denied by upstream server.'

class UnhandledOrder(APIException):
	status_code = status.HTTP_400_BAD_REQUEST
	default_detail = 'Unhandled Orders'
