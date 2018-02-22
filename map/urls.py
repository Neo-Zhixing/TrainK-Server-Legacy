from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AbstructMapView.as_view())
]
