from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
	path('', views.InfoHomeView.as_view(), name='info_home'),
]


router = routers.DefaultRouter()
router.register('station', views.StationViewSet)
router.register('train', views.TrainViewSet)
router.register('train/(?P<pk>[^/.]+)/record', views.RecordViewSet)
urlpatterns += router.urls
