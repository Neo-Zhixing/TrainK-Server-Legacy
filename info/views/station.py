from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .. import models, serializers


class StationView(APIView):
	template_name = 'station.html'

	def get(self, request):
		name = request.GET.get('name')
		telecode = request.GET.get('telecode')

		# 根据请求参数获取Station Object
		if name:
			station = get_object_or_404(models.Station, name=name)
		elif telecode:
			station = get_object_or_404(models.Station, telecode=telecode)
		else:
			all = request.GET.get('all')
			stations = models.Station.objects.all()
			data = dict((station.telecode, station.name) for station in stations if all or station.telecode is not '')
			return Response(data)

		serializer = serializers.StationSerializer(station)
		return Response(serializer.data)
