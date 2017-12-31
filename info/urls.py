from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	path('', TemplateView.as_view(template_name='info.html'), name='info_home'),
	path('station/', views.StationListView.as_view(), name='info_station_list'),
	path('station/<telecode>/', views.StationView.as_view(), name='info_station'),
	path('train/<telecode>/', views.TrainView.as_view(), name='info_train'),
	path('train/<telecode>/record/', views.RecordView.as_view(), name='info_record'),
]
