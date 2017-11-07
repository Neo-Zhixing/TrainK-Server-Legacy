from django.http import JsonResponse
from api import models

from django.conf.urls import url


def station(request):
	if request.method != 'GET':
		return JsonResponse({
			'result': False,
			'code': 405,
			'reason': 'Request method %s not allowed. Use GET.' % request.method
		})

	if request.GET.get('telecode'):
		condition = request.GET.get('telecode')
		stations = models.Station.objects.filter(telecode=condition)
	elif request.GET.get('name'):
		condition = request.GET.get('name')
		stations = models.Station.objects.filter(name=condition)
	else:
		return JsonResponse({
			'result': False,
			'code': 400,
			'reason': 'Parameters Illegal'
		})

	if stations:
		body = []
		for station in stations:
			body.append({
				'name': station.name,
				'telecode': station.telecode
			})
		if len(body) > 1:
			return JsonResponse({
				'result': False,
				'code': 500,
				'reason': ('Multiple stations found for %s' % condition),
				'body': body
			},
				json_dumps_params={
					'ensure_ascii': False
			})

		return JsonResponse(
			{
				'result': True,
				'code': 200,
				'body': body[0]
			},
			json_dumps_params={
				'ensure_ascii': False
			}
		)

	return JsonResponse({
		'result': False,
		'code': 404,
		'reason': 'Cannot find station for %s' % condition
	},
		json_dumps_params={
			'ensure_ascii': False
	})


def train(request):
	if request.method != 'GET':
		return JsonResponse({
			'result': False,
			'code': 405,
			'reason': 'Request method %s not allowed. Use GET.' % request.method
		})
	if request.GET.get('telecode'):
		condition = request.GET.get('telecode')
		trains = models.Train.objects.filter(telecode=condition)
	elif request.GET.get('name'):
		condition = request.GET.get('name')
		trains = models.Train.objects.filter(names__contains=[condition])
	else:
		return JsonResponse({
			'result': False,
			'code': 400,
			'reason': 'Parameters illegal'
		})

	if trains:
		if trains.count() > 1:
			return JsonResponse({
				'result': False,
				'code': 500,
				'reason': ('Multiple trains found for %s' % condition),
			},
				json_dumps_params={
					'ensure_ascii': False
			})

		train = trains[0]
		schedule = []
		for stop in train.stops.all():
			schedule.append({
				'stationName': stop.station.name,
				'stationTelecode': stop.station.telecode,
				'departureTime': stop.departureTime,
				'arrivalTime': stop.arrivalTime
			})
		body = {
			'name': train.names,
			'telecode': train.telecode,
			'schedule': schedule
		}
		return JsonResponse(
			{
				'result': True,
				'code': 200,
				'body': body
			},
			json_dumps_params={
				'ensure_ascii': False
			}
		)

	return JsonResponse({
		'result': False,
		'code': 404,
		'reason': 'Cannot find station for %s' % condition
	},
		json_dumps_params={
			'ensure_ascii': False
	})


urlpatterns = [
	url(r'^station$', station, name='query.station'),
	url(r'^train$', train, name='query.train'),
]
