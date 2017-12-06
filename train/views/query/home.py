from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render
from django import forms
from train import models

from django.urls import path

from copy import deepcopy


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

from train.views.query import train
urlpatterns = [
	path('', QueryHomeView.as_view()),
	path('station', station, name='query.station'),
	path('train', train.QueryTrainView.as_view()),
]
