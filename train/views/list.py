from django.http import JsonResponse
from train import models

from django.urls import path


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
	path('stations', stations, name='list.stations'),
	path('trains', trains, name='list.trainss'),
]
