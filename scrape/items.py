import scrapy
from scrapy_djangoitem import DjangoItem
from info import models


class Station(DjangoItem):
	django_model = models.Station
	save_batch_size = 100

	@property
	def duplicated(self):
		return models.Station.objects.filter(name=self['name']).exists()

	def duplicatedWillDiscard(self):
		originalStation = models.Station.objects.get(name=self['name'])
		if originalStation.telecode == '' and self['telecode'] != '':
			originalStation.telecode = self['telecode']
			originalStation.spell = self['spell']
			originalStation.abbreviation = self['abbreviation']
			originalStation.save()
			return 'Updated station %s telecode to %s' % (originalStation.name, originalStation.telecode)
		return 'Discarded'

	def __str__(self):
		return self['name']


class Train(DjangoItem):
	django_model = models.Train
	save_batch_size = 50

	def __str__(self):
		nameStr = ''
		for name in self['names']:
			nameStr += name + '/'
		return nameStr[:-1] + '|' + self['telecode']

	@property
	def duplicated(self):
		return models.Train.objects.filter(telecode=self['telecode']).exists()

	def itemWillCreate(self):
		for stop in self['stops']:
			station, _ = models.Station.objects.get_or_create(name=stop['station'])
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
			if stop.get('departureTime'):
				stop['departureTimeAnticipated'] = True
			if stop.get('arrivalTime'):
				stop['arrivalTimeAnticipated'] = True
			del stop['station']
			return stop

		self['stops'] = [setTimeAnticipated(stop) for stop in self['train'].stops]
