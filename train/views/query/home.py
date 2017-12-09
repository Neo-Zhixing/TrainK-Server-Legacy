from django.views.generic import TemplateView
from django.shortcuts import render
from django import forms
from django.urls import path

from copy import deepcopy


from train.views.query import station, train, home


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
	path('', home.QueryHomeView.as_view()),
	path('station', station.StationView.as_view()),
	path('train', train.TrainView.as_view()),
	path('record', train.RecordView.as_view()),
]
