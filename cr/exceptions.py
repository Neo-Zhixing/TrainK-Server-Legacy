from rest_framework.exceptions import APIException


class UpstreamRefused(APIException):
	status_code = 502
	default_detail = 'Upstream server refused the request.'
	default_code = 'service_unavailable'
