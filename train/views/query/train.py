from django.views.generic import TemplateView
from django.views.defaults import page_not_found
from django.shortcuts import render

from train import models

class QueryTrainView(TemplateView):
	template_name = 'query-train.html'

	def getTrain(self, name=None, telecode=None):
		if telecode:
			train = models.Train.objects.filter(telecode=telecode).first()
		elif name:
			train = models.Train.objects.filter(names__contains=[name]).first()
		else:
			return 'NoParameters'

		def convertStopStation(stop):
			station = models.Station.objects.get(id=stop['station'])
			stop['station'] = station.name
			stop['telecode'] = station.telecode
			return stop

		def delStopStationInfo(stop):
			stop.pop('station')
			return stop

		if train:
			return train
			body = {
				'name': train.names,
				'telecode': train.telecode,
				'schedule': list(map(convertStopStation, train.stops))
			}
			date = request.GET.get('date')
			if date:
				match = re.match(r'^r(\d+)$', date)
				if match:
					days = int(match.group(1))
					records = models.Record.objects.filter(train=train, departureDate__gte=timezone.now() - datetime.timedelta(days=days))
				else:
					dates = date.split('|')
					records = models.Record.objects.filter(train=train, departureDate__in=dates)

				body['records'] = {}
				for record in records:
					body['records'][record.departureDate.isoformat()] = list(map(delStopStationInfo, record.stops))

			return JsonResponse(
				{
					'result': True,
					'code': 200,
					'body': body
				},
				json_dumps_params={
					'ensure_ascii': False
				}
			)

	def get(self, request):
		if not request.GET.get('name'):
			return page_not_found(request, exception='Parameters')
		train = self.getTrain(name=request.GET['name'])
		if not train:
			return page_not_found(request, exception='Parameters')

		return render(request, self.template_name, {'train': train})
