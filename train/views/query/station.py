from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.defaults import page_not_found

from train import models, serializers


class StationView(APIView):
	template_name = 'query-train.html'

	def get(self, request):
		name = request.GET.get('name')
		telecode = request.GET.get('telecode')

		# 根据请求参数获取Station Object
		if name:
			station = models.Station.objects.filter(name=name).first()
		elif telecode:
			station = models.Station.objects.filter(telecode=telecode).first()
		else:
			return page_not_found(request, exception='Invalid Parameters')

		if not station:
			return page_not_found(request, exception='Train Not Found')

		serializer = serializers.StationSerializer(station)
		return Response(serializer.data)
