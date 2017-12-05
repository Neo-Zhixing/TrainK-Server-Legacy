from django.urls import include, path
from train.views import home

urlpatterns = [
	path('', home.HomeView.as_view()),
	path('list/', include('train.views.list')),
	path('query/', include('train.views.query')),
]
