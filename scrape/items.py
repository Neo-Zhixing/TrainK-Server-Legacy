import scrapy
from scrapy_djangoitem import DjangoItem
from api import models


class Station(DjangoItem):
	django_model = models.Station

	@property
	def duplicated(self):
		return models.Station.objects.filter(name=self['name'], telecode=self['telecode']).exists()

	def __str__(self):
		return self['name']


class Train(DjangoItem):
	django_model = models.Train
	name = scrapy.Field()

	def __str__(self):
		return self['name'] + ' | ' + self['telecode']

	@property
	def duplicated(self):
		return models.Train.objects.filter(telecode=self['telecode']).exists()

	def duplicatedWillDiscard(self):
		originalTrain = models.Train.objects.filter(telecode=self['telecode']).first()
		if self['name'] in originalTrain.names:
			return '%s, telecode %s' % (self['name'], self['telecode'])
		else:
			originalTrain.names.append(self['name'])
			originalTrain.save()
			return 'Merged with %s, telecode %s' % (originalTrain.name, originalTrain.telecode)

	def itemWillCreate(self):
		self['names'] = [self['name']]


class Record(DjangoItem):
	django_model = models.Record
	telecode = scrapy.Field()

	def __str__(self):
		return self['telecode'] + ' on ' + self['departureDate']

	@property
	def duplicated(self):
		return models.Record.objects.filter(departureDate=self['departureDate'], train__telecode=self['telecode']).exists()

	def itemWillCreate(self):
		query = models.Train.objects.filter(telecode=self['telecode'])
		if not query.exists():
			return 'Train %s not exist!' % self['telecode']
		self['train'] = query.first()

		def setTimeAnticipated(stop):
			stop['departureTime'] = -stop['departureTime'] if stop['departureTime'] else None
			stop['arrivalTime'] = -stop['arrivalTime'] if stop['arrivalTime'] else None
			return stop

		self['stops'] = [setTimeAnticipated(stop) for stop in self['train'].stops]
