from django.db import models
from django.contrib.postgres.fields import ArrayField


class Station(models.Model):
	name = models.CharField(max_length=10)
	telecode = models.CharField(max_length=5, blank=True)


class Stop(models.Model):
	station = models.ForeignKey(Station)
	departureTime = models.DurationField(blank=True, null=True)
	arrivalTime = models.DurationField(blank=True, null=True)

	@property
	def relatedTrain(self):
		if hasattr(self, 'train'):
			return self.train
		if hasattr(self, 'record'):
			return self.record.train
		return None

	def __str__(self):
		return '%s(%s - %s)' % (self.station.name, self.arrivalTime, self.departureTime)


class Train(models.Model):
	names = ArrayField(models.CharField(max_length=10))
	telecode = models.CharField(max_length=50)
	stops = models.ManyToManyField(Stop, related_name='train')

	@property
	def name(self):
		nameStr = ''
		for name in self.names:
			nameStr += name + '/'
		return nameStr[:-1]


class Record(models.Model):
	departureDate = models.DateField()
	train = models.ForeignKey(Train)
	stops = models.ManyToManyField(Stop, related_name='record')
