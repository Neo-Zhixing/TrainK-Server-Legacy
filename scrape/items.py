import scrapy
from scrapy_djangoitem import DjangoItem
from api import models


class Station(DjangoItem):
	django_model = models.Station
	save_batch_size = 100

	@property
	def duplicated(self):
		return models.Station.objects.filter(name=self['name'], telecode=self['telecode']).exists()

	def __str__(self):
		return self['name']


class Train(DjangoItem):
	django_model = models.Train
	save_batch_size = 50
	name = scrapy.Field()

	def __str__(self):
		return self['name'] + ' | ' + self['telecode']

	@property
	def duplicated(self):
		return models.Train.objects.filter(telecode=self['telecode']).exists()

	def duplicatedWillDiscard(self):
		originalTrain = models.Train.objects.get(telecode=self['telecode'])
		if self['name'] in originalTrain.names:
			return '%s, telecode %s' % (self['name'], self['telecode'])
		else:
			originalTrain.names.append(self['name'])
			originalTrain.save()
			return 'Merged with %s, telecode %s' % (originalTrain.name, originalTrain.telecode)

	def itemWillCreate(self):
		self['names'] = [self['name']]
		for stop in self['stops']:
			station = models.Station.objects.filter(name=stop['station'])
			if station.exists():
				station = station.first()
			else:
				station = models.Station.objects.create(name=stop['station'])
			stop['station'] = station.id


class Record(DjangoItem):
	django_model = models.Record
	telecode = scrapy.Field()
	save_batch_size = 50

	def __str__(self):
		return self['telecode'] + ' on ' + self['departureDate']

	@property
	def duplicated(self):
		return models.Record.objects.filter(departureDate=self['departureDate'], train__telecode=self['telecode']).exists()

	def itemWillCreate(self):
		self['train'] = models.Train.objects.get(telecode=self['telecode'])

		def setTimeAnticipated(stop):
			stop['departureTime'] = -stop['departureTime'] if stop['departureTime'] else None
			stop['arrivalTime'] = -stop['arrivalTime'] if stop['arrivalTime'] else None
			return stop

		self['stops'] = [setTimeAnticipated(stop) for stop in self['train'].stops]
