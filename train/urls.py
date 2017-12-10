from django.urls import include, path

urlpatterns = [
	path('', include('train.views.home')),
	path('query/', include('train.views.query.home')),
	path('map/', include('train.views.map')),
]
