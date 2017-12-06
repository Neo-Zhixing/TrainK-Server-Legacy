from django.views.generic import TemplateView
from django.urls import path


class MapView(TemplateView):
	template_name = "map.html"


urlpatterns = [
	path('', MapView.as_view()),
]
