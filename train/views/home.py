from django.views.generic import TemplateView
from django.urls import path


class HomeView(TemplateView):
	template_name = "home.html"


urlpatterns = [
	path('', HomeView.as_view()),
]
