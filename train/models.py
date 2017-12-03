from django.db import models
from django.contrib.postgres import fields
from django.core.serializers.json import DjangoJSONEncoder
import enum


class Station(models.Model):
	name = models.CharField(max_length=10)
	telecode = models.CharField(max_length=5, blank=True)


class Train(models.Model):
	names = fields.ArrayField(models.CharField(max_length=10))
	telecode = models.CharField(max_length=50, primary_key=True)
	stops = fields.JSONField(encoder=DjangoJSONEncoder)

	def __str__(self):
		return self.name

	@property
	def name(self):
		nameStr = ''
		for name in self.names:
			nameStr += name + '/'
		return nameStr[:-1]


class Record(models.Model):
	departureDate = models.DateField()
	train = models.ForeignKey(Train, on_delete=models.CASCADE)
	stops = fields.JSONField(encoder=DjangoJSONEncoder)


class Stop(models.Model):
	train = models.ForeignKey(Train, on_delete=models.PROTECT)
	record = models.ForeignKey(Record, on_delete=models.PROTECT)
	station = models.ForeignKey(Station, on_delete=models.PROTECT)
	index = models.IntegerField(primary_key=True)

	# Both time and anticipated indicator are None:
	# 	This stop is the origin or destination stop, so the arrival/departure time is not available.
	# Anticipated indicator is None, while time has value:
	# 	The program cannot fetch the information about this stop. NotImplemented or TimeNotInRange Errer
	# Both Anticipated indicator and time have value:
	# 	Anticipated indicator is True: the delays information is yet to be scraped.
	# 	Anticipated indicator is False: the information is accurately scraped.

	departureTime = models.DateTimeField()
	departureTimeAnticipated = models.BooleanField()
	arrivalTime = models.DateTimeField()
	arrivalTimeAnticipated = models.BooleanField()

	class Meta:
		managed = False

	def update(self, action, time='NoChange', anticipated='NoChange'):
		key = 'departureTime' if action == TrainAction.Departure else 'arrivalTime'
		if time is not 'NoChange':
			self.record.stops[self.index][key] = time
			setattr(self, key, time)
		if anticipated is not 'NoChange':
			key = key + 'Anticipated'
			self.record.stops[self.index][key] = anticipated
			setattr(self, key, anticipated)
		self.record.save()


class TrainAction(enum.Enum):
		Departure = 1
		Arrival = 0
