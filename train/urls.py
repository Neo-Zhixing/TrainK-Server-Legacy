from django.conf.urls import url, include

urlpatterns = [
	url(r'^list/', include('train.views.list')),
	url(r'^query/', include('train.views.query')),
]
