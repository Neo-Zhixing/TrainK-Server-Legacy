from django.views.defaults import bad_request
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_duration
from django.utils.duration import duration_iso_string
from datetime import timedelta
from enum import Enum, auto
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
			response = self.paginator.get_paginated_response(serializers.TrainSerializer(train, many=True, stops=False).data)
			response.template_name = 'query-train.html'
			return response

		# 通过站点ID/Telecode/中文名查找两个站点之间的所有列车
		departureID = _getStationID(request.GET, 'departure')
		arrivalID = _getStationID(request.GET, 'arrival')
		if departureID and arrivalID:
			train = models.Train.objects.filter(stops__contains=[{'station': departureID}, {'station': arrivalID}])
			train = self.paginator.paginate_queryset(train, request)
			response = self.paginator.get_paginated_response(serializers.TrainSerializer(train, many=True, stops=False).data)
			response.template_name = 'query-train.html'
			return response

		return bad_request(request, None)

	@property
	def paginator(self):
		if not hasattr(self, '_paginator'):
				self._paginator = api_settings.DEFAULT_PAGINATION_CLASS()
		return self._paginator


class RecordView(APIView):
	template_name = 'record.html'

	class Action(Enum):
		Basic = auto()     # Actual or anticipated departure/arrival time
		Details = auto()   # Departure/arrival time according to the schedule
		Analysis = auto()  # On-schedule rates and mean delay time in a day
		Train = auto()

	def get(self, request):
		train = _getTrain(request.GET)
		records = models.Record.objects.filter(train=train).order_by('-departureDate')
		records = self.paginator.paginate_queryset(records, request)

		if 'actions' in request.GET:
			actions = request.GET['actions'].split('|')
			actions = set(self.Action[action.title()] for action in actions)
		else:
			actions = set(self.Action)

		# TODO: Optimize by making all these actions in Database Side.
		records = serializers.RecordSerializer(records, many=True).data

		for record in records:
			delaySum = timedelta()
			count = 0
			for index, stop in enumerate(record['stops']):
				for key in ['arrival', 'departure']:
					timeKey = key + 'Time'
					delayKey = key + 'Delay'
					if timeKey not in stop:
						continue
					delay = parse_duration(stop[timeKey]) - parse_duration(train.stops[index][timeKey])
					if self.Action.Basic not in actions:
						del stop[timeKey]
					if self.Action.Details in actions:
						stop[delayKey] = duration_iso_string(delay)
					delaySum += delay
				count += 1
			if self.Action.Analysis in actions:
				flag = 1
				if delaySum < timedelta():
					delaySum *= -1
					flag = -1
				record['delayAvg'] = round(delaySum.seconds / (flag * count * 120), 2)
				if len(actions) is 1:
					del record['stops']

		response = self.paginator.get_paginated_response(records)
		if self.Action.Train in actions:
			response.data['train'] = serializers.TrainSerializer(train).data
		return response

	class Pagination(api_settings.DEFAULT_PAGINATION_CLASS):
		page_size = 7

	@property
	def paginator(self):
		if not hasattr(self, '_paginator'):
			self._paginator = self.Pagination()
		return self._paginator
