from django.urls import path
from django.views.generic import TemplateView

from .views import station, train

urlpatterns = [
	path('', TemplateView.as_view(template_name='info.html')),
	path('station', station.StationView.as_view()),
	path('train', train.TrainView.as_view()),
	path('record', train.RecordView.as_view()),
]
