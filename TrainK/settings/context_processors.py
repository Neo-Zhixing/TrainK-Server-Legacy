from django.conf import settings

def mode(context):
	return {'DEBUG_MODE': settings.MODE}
