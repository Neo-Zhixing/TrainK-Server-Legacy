from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from . import models, serializers

from django.views.defaults import bad_request
from django.utils.dateparse import parse_duration
from django.utils.duration import duration_iso_string
from datetime import timedelta
from enum import Enum, auto
from rest_framework.settings import api_settings


def _browserRequest(request):
	# The lack of accepted renderer indicates that the content negotiation failed,
	# in which case the rest framework will always use the first renderer, TemplateHTMLRenderer.
	# That's why we directly return True here.
	if not hasattr(request, 'accepted_renderer'):
		return True
	return isinstance(request.accepted_renderer, TemplateHTMLRenderer)


class PaginationMixin:
	pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

	@property
	def paginator(self):
		if not hasattr(self, '_paginator'):
				self._paginator = self.pagination_class()
		return self._paginator


class StationView(APIView):
	template_name = 'station.html'

	def get(self, request, telecode):
		queryType = request.GET.get('type')
		if queryType is None:
			queryType = 'telecode'  # Default queryType is telecode

		if queryType is 'name':  # Redirect name queries
			station = get_object_or_404(models.Station, name=telecode)
			return redirect('info_station', station.id if station.telecode == '' else station.telecode)
		elif queryType is 'id':  # Redirect id queries if the station has a telecode
			station = get_object_or_404(models.Station, id=telecode)
			if station.telecode != '':
				return redirect('info_station', station.telecode)
		elif queryType is 'telecode':
			station = get_object_or_404(models.Station, telecode=telecode)
		else:
			return bad_request(request, 'Illegal Query Type')

		return Response(station if _browserRequest(request) else serializers.StationSerializer(station).data)


class StationListView(APIView, PaginationMixin):

	def get(self, request):
		stations = models.Station.objects.all()
		stations = self.paginator.paginate_queryset(stations, request)

		if _browserRequest(request):
			data = stations
		else:
			serializer = serializers.StationSerializer(stations, many=True)
			data = serializer.data
		return self.paginator.get_paginated_response(data)


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


class TrainView(APIView):

	def get(self, request, telecode):
		queryType = request.GET.get('type')
		if not queryType:
			queryType = 'telecode'  # Default queryType is teleocode

		if queryType is 'name':
			train = get_list_or_404(models.Train, names__contains=[telecode]).latest('since')
			return redirect('info_train', train.telecode)
		elif queryType is 'telecode':
			train = get_object_or_404(models.Train, telecode=telecode)
		else:
			return bad_request(request, 'Illegal Query Type')

		return Response(train if _browserRequest(request) else serializers.TrainSerializer(train).data)


class TrainListView(APIView):
	def get(self, request, telecode):
		# 通过站点ID/Telecode/中文名查找经过该站点的所有列车
		stationID = _getStationID(request.GET, 'station')
		if stationID:
			train = models.Train.objects.filter(stops__contains=[{'station': stationID}])
			train = self.paginator.paginate_queryset(train, request)
			response = self.paginator.get_paginated_response(serializers.TrainSerializer(train, many=True, serializeStops=False).data)
			return response

		# 通过站点ID/Telecode/中文名查找两个站点之间的所有列车
		departureID = _getStationID(request.GET, 'departure')
		arrivalID = _getStationID(request.GET, 'arrival')
		if departureID and arrivalID:
			train = models.Train.objects.filter(stops__contains=[{'station': departureID}, {'station': arrivalID}])
			trainsToExclude = []
			for i in train:
				for index, stop in enumerate(i.stops):
					if stop['station'] == departureID:
						departureIndex = index
					elif stop['station'] == arrivalID:
						arrivalIndex = index
				if departureIndex > arrivalIndex:
					trainsToExclude.append(i.telecode)
			for telecode in trainsToExclude:
				train = train.exclude(telecode=telecode)
			train = self.paginator.paginate_queryset(train, request)
			response = self.paginator.get_paginated_response(
				serializers.TrainSerializer(
					train,
					many=True,
					serializeStops=False,
					includingStops={departureID: 'departureStop', arrivalID: 'arrivalStop'})
				.data
			)
			response.template_name = 'route.html'
			return response

		return bad_request(request, None)

	@property
	def paginator(self):
		if not hasattr(self, '_paginator'):
				self._paginator = api_settings.DEFAULT_PAGINATION_CLASS()
		return self._paginator


class RecordView(APIView, PaginationMixin):
	template_name = 'record.html'

	class Action(Enum):
		Basic = auto()     # Actual or anticipated departure/arrival time
		Details = auto()   # Departure/arrival time according to the schedule
		Analysis = auto()  # On-schedule rates and mean delay time in a day
		Train = auto()

	def get(self, request, telecode):
		train = get_object_or_404(models.Train, telecode=telecode)
		records = get_list_or_404(models.Record, train__telecode=telecode).order_by('-departureDate')
		records = self.paginator.paginate_queryset(records, request)

		if _browserRequest(request):
			return Response({'records': records})

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
	pagination_class = Pagination()
