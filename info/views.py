from collections import OrderedDict
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.http import Http404
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import FormView
from . import models, serializers
from utils.mixins import VersatileViewMixin

from django.views.generic import ListView, DetailView
from django.utils.dateparse import parse_duration


def GetStation(key, queryset=models.Station.objects):
	if key.isnumeric():
		return get_object_or_404(queryset, id=key)

	if queryset.filter(telecode=key).exists():
		return queryset.get(telecode=key)

	return get_object_or_404(queryset, name=key)


def GetTrain(key, queryset=models.Train.objects):
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


class HomeTabForm(forms.Form):
	action = forms.IntegerField(widget=forms.HiddenInput(), initial=0, min_value=0, max_value=3)
	route_from = forms.CharField(max_length=10, required=False)
	route_to = forms.CharField(max_length=10, required=False)
	train = forms.CharField(max_length=20, required=False)
	station = forms.CharField(max_length=10, required=False)
	line = forms.CharField(max_length=20, required=False)

	def clean(self):
		cleaned_data = super().clean()
		action = cleaned_data['action']
		if action == 0:
			actionContent = cleaned_data['route_from'] + '或' + cleaned_data['route_to'] \
				if cleaned_data['route_from'] and cleaned_data['route_to'] else False
		else:
			actionContent = cleaned_data[['train', 'station', 'line'][action - 1]]
		newValue = {}
		if not actionContent:
			raise ValidationError(
				('您没有填写相关查询条件'),
				code='empty'
			)
		try:
			if action == 1:
				newValue['value'] = GetTrain(cleaned_data['train'])
			elif action == 2:
				newValue['value'] = GetStation(cleaned_data['station'])
			elif action == 0:
				newValue['value'] = (GetStation(cleaned_data['route_from']), GetStation(cleaned_data['route_to']))
		except (NotFound, Http404):
			raise ValidationError(
				('没有找到 %(value)s'),
				code='notfound',
				params={'value': actionContent},
			)
		else:
			newValue['action'] = action
		return newValue

	def __init__(self, *args, **kwargs):
		super(HomeTabForm, self).__init__(*args, **kwargs)
		self.fields['train'].widget.attrs['placeholder'] = 'G7'
		self.fields['station'].widget.attrs['placeholder'] = '合肥南'
		self.fields['line'].widget.attrs['placeholder'] = '京津城际'


class InfoHomeView(FormView):
	template_name = 'info.html'
	form_class = HomeTabForm

	def form_valid(self, form):
		action = form.cleaned_data['action']
		value = form.cleaned_data['value']
		if action == 1:  # train
			return redirect('train-detail', value.telecode)
		if action == 2:  # station
			return redirect('station-detail', value.telecode if value.telecode else value.id)
		if action == 3:
			return redirect()


class StationDetailTemplateView(DetailView):
	template_name = 'station.html'
	model = models.Station

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		return GetStation(self.kwargs[self.pk_url_kwarg], queryset)

	def get_context_data(self, object, *args, **kwargs):
		data = super(StationDetailTemplateView, self).get_context_data(object=object, *args, **kwargs)
		data['trains'] = models.Train.objects.filter(stops__contains=[{'station': data['station'].pk}])
		for train in data['trains']:
			for stop in train.stops:
				if stop['station'] == object.id:
					train.currentStop = stop
					break
		return data

	def get(self, request, *args, **kwargs):
		pk = self.kwargs[self.pk_url_kwarg]
		station = self.get_object()
		if station.name == pk:  # Query based on station name
			return redirect('station-detail', pk=station.id if station.telecode == '' else station.telecode, permanent=True)
		if pk.isnumeric() and station.telecode != '':  # Rediret id based queries when the station has a telecode
			return redirect('station-detail', pk=station.telecode, permanent=True)
		self.object = station
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)


class StationViewSet(OptionalPaginationMixin, VersatileViewMixin, viewsets.ReadOnlyModelViewSet):
	queryset = models.Station.objects.all()
	serializer_class = serializers.StationSerializer
	template_views = {
		'retrieve': StationDetailTemplateView.as_view()
	}

	def get_queryset(self):
		queryset = super(StationViewSet, self).get_queryset()
		if 'all' in self.request.query_params and self.request.query_params['all'].lower() == 'true':
			return queryset
		return queryset.exclude(telecode='')

	def get_object(self):
		return GetStation(self.kwargs[self.lookup_field], self.queryset)


class TrainDetailTemplateView(DetailView):
	template_name = 'train.html'
	model = models.Train

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		return GetTrain(self.kwargs[self.pk_url_kwarg], queryset)

	def get(self, request, *args, **kwargs):
		# Redirect queries using train names
		pk = self.kwargs[self.pk_url_kwarg]
		train = self.get_object()
		if pk in train.names:
			return redirect('train-detail', pk=train.telecode, permanent=True)
		self.object = train
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)


class TrainViewSet(VersatileViewMixin, viewsets.ReadOnlyModelViewSet):
	queryset = models.Train.objects.all()
	template_views = {
		'retrieve': TrainDetailTemplateView.as_view()
	}

	def get_serializer_class(self):
		return serializers.TrainListSerializer if self.action == 'list' else serializers.TrainDetailSerializer

	def get_object(self):
		return GetTrain(self.kwargs[self.lookup_field], self.queryset)

	def get_queryset(self):
		queryset = super(TrainViewSet, self).get_queryset()
		if 'station' in self.request.query_params:
			station = GetStation(self.request.query_params['station'])
			return queryset.filter(stops__contains=[{'station': station.pk}])

		if 'from' in self.request.query_params and 'to' in self.request.query_params:
			fromStation = GetStation(self.request.query_params['from'])
			toStation = GetStation(self.request.query_params['to'])
			trains = queryset.filter(stops__contains=[{'station': fromStation.pk}, {'station': toStation.pk}])
			results = trains
			for train in trains:
				departureIndex = None
				arrivalIndex = None
				for index, stop in enumerate(train.stops):
					if stop['station'] == fromStation.pk:
						departureIndex = index
					elif stop['station'] == toStation.pk:
						arrivalIndex = index
				if departureIndex and arrivalIndex and departureIndex > arrivalIndex:
					results = results.exclude(telecode=train.telecode)
			return results
		return queryset


class RecordListTemplateView(ListView):
	template_name = 'record.html'
	model = models.Record
	train_url_kwarg = 'pk'

	@property
	def train(self):
		if not hasattr(self, '_train'):
			self._train = GetTrain(self.kwargs[self.train_url_kwarg])
		return self._train

	def get_queryset(self):
		return super(RecordListTemplateView, self).get_queryset().filter(train__names=self.train.names).order_by('-departureDate')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		train = self.train
		table = OrderedDict()
		# make horizontal table data
		for record in context['object_list']:
			for index, stop in enumerate(record.stops):
				stationID = train.stops[index]['station']
				plannedStop = train.stops[index]
				if stationID not in table:
					table[stationID] = []
				for action in models.TrainAction:
					key = action.name.lower()
					timeKey = key + 'Time'
					if timeKey in plannedStop and timeKey in stop:
						delay = parse_duration(stop[timeKey]) - parse_duration(plannedStop[timeKey])
						stop[key + 'Delay'] = round(delay.total_seconds() / 60)
						stop[timeKey] = parse_duration(stop[timeKey])
				table[stationID].append(stop)
		context['train'] = train
		context['table'] = table
		return context

	def get(self, request, *args, **kwargs):
		if self.kwargs[self.train_url_kwarg] in self.train.names:
			return redirect('record-list', pk=self.train.telecode, permanent=True)
		return super(RecordListTemplateView, self).get(request, *args, **kwargs)


class RecordViewSet(VersatileViewMixin, viewsets.ReadOnlyModelViewSet):
	queryset = models.Record.objects.all()
	lookup_field = 'departureDate'
	template_views = {
		'list': RecordListTemplateView.as_view()
	}

	def get_serializer_class(self):
		return serializers.RecordListSerializer if self.action == 'list' else serializers.RecordDetailSerializer

	def get_queryset(self):
		train = GetTrain(self.kwargs['pk'])
		return super(RecordViewSet, self).get_queryset().filter(train__names=train.names).order_by('-departureDate')
