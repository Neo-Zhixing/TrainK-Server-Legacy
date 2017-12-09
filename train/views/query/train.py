from django.views.defaults import bad_request
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from train import models, serializers


def _getStationID(args, name):
		station_id = None
		station = None

		name += '_'
		name_id = name + 'id'
		name_telecode = name + 'telecode'
		name_name = name + 'name'
		if name_id in args:
			station_id = args[name_id]
		elif name + 'name' in args:
			station = get_object_or_404(models.Station, name=args[name_name])
		elif name + 'telecode' in args:
			station = get_object_or_404(models.Station, telecode=args[name_telecode])
		if station:
			station_id = station.id
		return station_id


def _getTrain(args):
	train = None
	if 'name' in args:
		train = get_object_or_404(models.Train, names__contains=[args['name']])
	elif 'telecode' in args:
		train = get_object_or_404(models.Train, telecode=args['telecode'])
	return train


class TrainView(APIView):
	def get(self, request):
		# 通过列车名或Telecode查找单个列车
		train = _getTrain(request.GET)
		if train:
			return Response(serializers.TrainSerializer(train).data, template_name='query-train.html')

		# 通过站点ID/Telecode/中文名查找经过该站点的所有列车
		stationID = _getStationID(request.GET, 'station')
		if stationID:
			train = models.Train.objects.filter(stops__contains=[{'station': stationID}])
			train = self.paginator.paginate_queryset(train, request)
			return Response(serializers.TrainSerializer(train, many=True, stops=False).data, template_name='query-train.html')

		# 通过站点ID/Telecode/中文名查找两个站点之间的所有列车
		departureID = _getStationID(request.GET, 'departure')
		arrivalID = _getStationID(request.GET, 'arrival')
		if departureID and arrivalID:
			train = models.Train.objects.filter(stops__contains=[{'station': departureID}, {'station': arrivalID}])
			train = self.paginator.paginate_queryset(train, request)
			return Response(serializers.TrainSerializer(train, many=True, stops=False).data, template_name='query-train.html')

		return bad_request(request, None)

	pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

	@property
	def paginator(self):
		if not hasattr(self, '_paginator'):
			if self.pagination_class is None:
				self._paginator = None
			else:
				self._paginator = self.pagination_class()
		return self._paginator


class RecordView(APIView):
	def get(self, request):
		records = None
		train = _getTrain(request.GET)

		if request.GET.get('recent').isnumeric():
			days = int(request.GET['recent'])
			records = models.Record.objects.filter(train=train, departureDate__gte=timezone.now() - timedelta(days=days))

		if 'dates' in request.GET:
			dates = request.GET['dates'].split('|')
			records = models.Record.objects.filter(train=train, departureDate__in=dates)

		if records:
			return Response(serializers.RecordSerializer(records, many=True).data, template_name='query-train.html')

		return bad_request(request, None)
