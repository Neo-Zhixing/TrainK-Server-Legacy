from django.conf.urls import url, include

urlpatterns = [
	url(r'^list/', include('api.views.list')),
	url(r'^query/', include('api.views.query')),
]
