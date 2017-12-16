from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.defaults import bad_request
from train import models, serializers


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
			return bad_request(request, None)

		serializer = serializers.StationSerializer(station)
		return Response(serializer.data)
