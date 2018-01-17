from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from . import views

urlpatterns = [
	path('', TemplateView.as_view(template_name='info.html'), name='info_home'),
]


router = routers.DefaultRouter()
router.register('station', views.StationViewSet)
router.register('train', views.TrainViewSet)
router.register('train/(?P<pk>[^/.]+)/record', views.RecordViewSet)
urlpatterns += router.urls
