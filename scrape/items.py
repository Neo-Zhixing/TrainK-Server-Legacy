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


class Train(scrapy.Item):
	name = scrapy.Field()
	telecode = scrapy.Field()
	stops = scrapy.Field()

	def __str__(self):
		return self['name'] + ' | ' + self['telecode']

	@property
	def originalTrain(self):
		return models.Train.objects.filter(telecode=self['telecode']).first()


class Stop(scrapy.Item):
	station = scrapy.Field()
	arrivalTime = scrapy.Field()
	departureTime = scrapy.Field()
