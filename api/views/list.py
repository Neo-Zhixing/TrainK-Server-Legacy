from django.http import JsonResponse
from api import models

from django.conf.urls import url


def stations(request):
	body = []
	for station in models.Station.objects.all():
		body.append({
			'name': station.name,
			'telecode': station.telecode
		})
	return JsonResponse(
		{
			'body': body
		},
		json_dumps_params={
			'ensure_ascii': False
		}
	)


def trains(request):
	body = []
	for train in models.Train.objects.all():
		body.append({
			'names': train.names,
			'telecode': train.telecode
		})
	return JsonResponse(
		{
			'body': body
		},
		json_dumps_params={
			'ensure_ascii': False
		}
	)


urlpatterns = [
	url(r'^stations$', stations, name='list.stations'),
	url(r'^trains$', trains, name='list.trainss'),
]
