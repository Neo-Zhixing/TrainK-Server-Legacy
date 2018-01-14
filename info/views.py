from collections import OrderedDict
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from . import models, serializers

from django.views.defaults import bad_request
from django.utils.dateparse import parse_duration
from django.utils.duration import duration_iso_string
from datetime import timedelta


def _browserRequest(request):
	# The lack of accepted renderer indicates that the content negotiation failed,
	# in which case the rest framework will always use the first renderer, TemplateHTMLRenderer.
	# That's why we directly return True here.
	if not hasattr(request, 'accepted_renderer'):
		return True
	return isinstance(request.accepted_renderer, TemplateHTMLRenderer)


def _getStation(key, queryset):
	if key.isnumeric():
		return get_object_or_404(queryset, id=key)

	if queryset.filter(telecode=key).exists():
		return queryset.get(telecode=key)

	return get_object_or_404(queryset, name=key)


def _getTrain(key, queryset):
	if queryset.filter(telecode=key).exists():
		return queryset.get(telecode=key)
	train = queryset.filter(names__contains=[key])
	if train.exists():
		return train.latest('since')
	raise NotFound()


class OptionalPaginationMixin:
	@property
	def paginator(self):
		paginator = super(OptionalPaginationMixin, self).paginator
		param = self.request.query_params.get(paginator.page_query_param)
		if param is None or param is 0:
			return None
		return paginator


class StationViewSet(OptionalPaginationMixin, viewsets.ReadOnlyModelViewSet):
	template_name = 'station.html'
	queryset = models.Station.objects.all()
	serializer_class = serializers.StationSerializer
	lookup_field = 'telecode'

	def get_queryset(self):
		queryset = super(StationViewSet, self).get_queryset()
		if 'all' in self.request.query_params and self.request.query_params['all'] == 'true':
			return queryset
		return queryset.exclude(telecode='')

	def get_object(self):
		return _getStation(self.kwargs[self.lookup_field], self.queryset)

	def retrieve(self, request, telecode=None):
		if telecode and _browserRequest(request):
			station = self.get_object()
			if station.name == telecode:  # Query based on station name
				return redirect('station-detail', telecode=station.id if station.telecode == '' else station.telecode, permanent=True)
			if telecode.isnumeric() and station.telecode != '':  # Rediret id based queries when the station has a telecode
				return redirect('station-detail', telecode=station.telecode, permanent=True)
			return Response({
				'station': station
			})
		return super(StationViewSet, self).retrieve(self, request, telecode=telecode)


class TrainViewSet(viewsets.ReadOnlyModelViewSet):
	template_name = 'train.html'
	queryset = models.Train.objects.all()
	station_queryset = models.Station.objects.all()
	serializer_class = serializers.TrainSerializer

	def get_object(self):
		return _getTrain(self.kwargs[self.lookup_field], self.queryset)

	def get_serializer(self, *args, **kwargs):
		if self.action == 'retrieve':
			kwargs['expandNested'] = True
		return super(TrainViewSet, self).get_serializer(*args, **kwargs)

	def get_queryset(self):
		queryset = super(TrainViewSet, self).get_queryset()
		if 'station' in self.request.query_params:
			station = _getStation(self.request.query_params['station'], self.station_queryset)
			return queryset.filter(stops__contains=[{'station': station.pk}])

		if 'from' in self.request.query_params and 'to' in self.request.query_params:
			fromStation = _getStation(self.request.query_params['from'], self.station_queryset)
			toStation = _getStation(self.request.query_params['to'], self.station_queryset)
			trains = queryset.filter(stops__contains=[{'station': fromStation.pk}, {'station': toStation.pk}])
			results = trains
			for train in trains:
				for index, stop in enumerate(train.stops):
					if stop['station'] == fromStation.pk:
						departureIndex = index
					elif stop['station'] == toStation.pk:
						arrivalIndex = index
				if departureIndex > arrivalIndex:
					results = results.exclude(telecode=train.telecode)
			return results
		return queryset

	def retrieve(self, request, *args, **kwargs):
		pk = kwargs.pop('pk')
		if pk and _browserRequest(request):
			train = self.get_object()
			if pk in train.names:
				return redirect('train-detail', pk=train.telecode, permanent=True)
			return Response({
				'train': train
			})
		return super(TrainViewSet, self).retrieve(self, request, *args, **kwargs)


class RecordView(ListAPIView):
	template_name = 'record.html'
	queryset = models.Record.objects.all()
	serializer_class = serializers.RecordSerializer

	def get_queryset(self):
		queryset = super(RecordView, self).get_queryset()
		queryset = queryset.filter(train__telecode=self.kwargs['telecode']).order_by('-departureDate')
		return queryset

	def list(self, request, telecode):
		if not _browserRequest(request):
			return super(RecordView, self).list(request, telecode)

		train = get_object_or_404(models.Train, telecode=telecode)
		queryset = self.filter_queryset(self.get_queryset())
		page = self.paginate_queryset(queryset)
		if page is None:
			page = queryset
		table = OrderedDict()
		# make horizontal table data
		for record in page:
			for index, stop in enumerate(record.stops):
				stationID = train.stops[index]['station']
				plannedStop = train.stops[index]
				if stationID not in table:
					table[stationID] = []
				for key in ('departure', 'arrival'):
					timeKey = key + 'Time'
					if timeKey in plannedStop and timeKey in stop:
						delay = parse_duration(plannedStop[timeKey]) - parse_duration(stop[timeKey])
						stop[key + 'Delay'] = delay.seconds / 60 + delay.days * 1440
						stop[timeKey] = parse_duration(stop[timeKey])
				table[stationID].append(stop)
		return Response({
			'records': page,
			'train': train,
			'table': table
		})
