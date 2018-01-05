from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from . import views

urlpatterns = [
	path('', TemplateView.as_view(template_name='info.html'), name='info_home'),
	path('train/<telecode>/record/', views.RecordView.as_view(), name='info_train_record'),
]


router = routers.DefaultRouter()
router.register('station', views.StationViewSet)
router.register('train', views.TrainViewSet)
urlpatterns += router.urls
