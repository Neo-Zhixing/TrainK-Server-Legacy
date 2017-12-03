from django.http import JsonResponse
from train import models

from django.conf.urls import url


def stations(request):
	return JsonResponse(
		{
			'body': [{
				'name': station.name,
				'telecode': station.telecode
			} for station in models.Station.objects.all()]
		},
		json_dumps_params={
			'ensure_ascii': False
		}
	)


def trains(request):
	return JsonResponse(
		{
			'body': [{
				'name': train.names,
				'telecode': train.telecode
			} for train in models.Train.objects.all()]
		},
		json_dumps_params={
			'ensure_ascii': False
		}
	)


urlpatterns = [
	url(r'^stations$', stations, name='list.stations'),
	url(r'^trains$', trains, name='list.trainss'),
]
