from django.views.generic import TemplateView
from django.urls import path
from django.shortcuts import redirect


class HomeView(TemplateView):
	template_name = "home.html"

	def get(self, request):
		return redirect('https://tra.ink/query')


urlpatterns = [
	path('', HomeView.as_view()),
]
