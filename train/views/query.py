from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render
from django import forms
from train import models

from django.urls import path

import re
from copy import deepcopy
from django.utils import timezone
import datetime


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
		train = models.Train.objects.filter(telecode=condition).first()
	elif request.GET.get('name'):
		condition = request.GET.get('name')
		train = models.Train.objects.filter(names__contains=[condition]).first()
	else:
		return JsonResponse({
			'result': False,
			'code': 400,
			'reason': 'Parameters illegal'
		})

	def convertStopStation(stop):
		station = models.Station.objects.get(id=stop['station'])
		stop['station'] = station.name
		stop['telecode'] = station.telecode
		return stop

	def delStopStationInfo(stop):
		stop.pop('station')
		return stop

	if train:
		body = {
			'name': train.names,
			'telecode': train.telecode,
			'schedule': list(map(convertStopStation, train.stops))
		}
		date = request.GET.get('date')
		if date:
			match = re.match(r'^r(\d+)$', date)
			if match:
				days = int(match.group(1))
				records = models.Record.objects.filter(train=train, departureDate__gte=timezone.now() - datetime.timedelta(days=days))
			else:
				dates = date.split('|')
				records = models.Record.objects.filter(train=train, departureDate__in=dates)

			body['records'] = {}
			for record in records:
				body['records'][record.departureDate.isoformat()] = list(map(delStopStationInfo, record.stops))

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


class QueryHomeView(TemplateView):
	class Form(forms.Form):
		name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'G100'}))

	class PathForm(forms.Form):
		origin = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control text-right', 'placeholder': '北京'}))
		destination = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control text-left', 'placeholder': '上海'}))

	template_name = 'query.html'

	def get(self, request, *args, **kwargs):
		forms = {'pathForm': self.PathForm()}
		theForm = self.Form()
		for (name, placeholder) in [
			('trainForm', 'G100'),
			('stationForm', '北京'),
			('railwayForm', '广深港高铁')]:
			newForm = deepcopy(theForm)
			newForm.fields['name'].widget.attrs['placeholder'] = placeholder
			forms[name] = newForm
		del theForm
		return render(request, self.template_name, forms)


urlpatterns = [
	path('', QueryHomeView.as_view()),
	path('station', station, name='query.station'),
	path('train', train, name='query.train'),
]
