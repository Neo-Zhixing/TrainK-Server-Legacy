from datetime import timedelta
import re
from django.utils import timezone
from django.views.defaults import page_not_found
from rest_framework.views import APIView
from rest_framework.response import Response

from train import models, serializers


class TrainView(APIView):
	template_name = 'query-train.html'

	def get(self, request):
		name = request.GET.get('name')
		telecode = request.GET.get('telecode')
		if name:
			train = models.Train.objects.filter(names__contains=[name]).first()
		elif telecode:
			train = models.Train.objects.filter(telecode=telecode).first()
		else:
			return page_not_found(request, exception='Invalid Parameters')

		if not train:
			return page_not_found(request, exception='Train Not Found')
		context = {'train': train}

		serializer = serializers.TrainSerializer(train)
		return Response(serializer.data)


		date = request.GET.get('date')
		if not date:
			date = 'r7'
		match = re.match(r'^r(\d+)$', date)
		if match:
			days = int(match.group(1))
			records = models.Record.objects.filter(train=train, departureDate__gte=timezone.now() - timedelta(days=days))
		else:
			dates = date.split('|')
			records = models.Record.objects.filter(train=train, departureDate__in=dates)
		context['records'] = records

		return render(request, self.template_name, context)
