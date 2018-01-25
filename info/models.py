from django.db import models
from django.contrib.postgres import fields
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import reverse
from django.utils.dateparse import parse_duration
from datetime import timedelta
import enum


class Station(models.Model):
	name = models.CharField(max_length=10)
	telecode = models.CharField(max_length=3, blank=True)
	abbreviation = models.CharField(max_length=10)
	spell = models.CharField(max_length=30)

	def get_absolute_url(self):
		return reverse('info_station')


class TrainAction(enum.Enum):
	Departure = 1
	Arrival = 0


class Train(models.Model):
	names = fields.ArrayField(models.CharField(max_length=10))
	telecode = models.CharField(max_length=12, primary_key=True)
	stops = fields.JSONField(encoder=DjangoJSONEncoder)
	since = models.DateField()

	def __str__(self):
		return self.name

	@property
	def name(self):
		return '/'.join(self.names)

	def get_absolute_url(self):
		return reverse('info_train')


class Record(models.Model):
	departureDate = models.DateField()
	train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='records')
	stops = fields.JSONField(encoder=DjangoJSONEncoder)

	@property
	def delay(self):
		grossDelay = timedelta()
		count = 0
		for index, stop in enumerate(self.stops):
			plannedStop = self.train.stops[index]
			for action in TrainAction:
				key = action.name.lower() + 'Time'
				if key not in stop or key not in plannedStop or stop[key + 'Anticipated']:
					continue
				count += 1
				delay = abs(parse_duration(stop[key]) - parse_duration(plannedStop[key]))
				grossDelay += delay
		if count == 0:
			return 0
		return grossDelay / count / 60

	def get_absolute_url(self):
		return reverse('info_record')


class Stop(models.Model):
	id = models.CharField(max_length=16, primary_key=True)
	index = models.IntegerField()
	record = models.ForeignKey(Record, on_delete=models.DO_NOTHING, related_name='getStops')

	@property
	def train(self):
		return self.record.train

	@property
	def station(self):
		stationID = self.scheduledStop['station']
		return Station.objects.get(pk=stationID)

	@property
	def scheduledStop(self):
		return self.train.stops[self.index]

	# Both time and anticipated indicator are None:
	# 	This stop is the origin or destination stop, so the arrival/departure time is not available.
	# Anticipated indicator is None, while time has value:
	# 	The program cannot fetch the information about this stop. NotImplemented or TimeNotInRange Errer
	# Both Anticipated indicator and time have value:
	# 	Anticipated indicator is True: the delays information is yet to be scraped.
	# 	Anticipated indicator is False: the information is accurately scraped.

	departureTime = models.DateTimeField(null=True)
	arrivalTime = models.DateTimeField(null=True)
	departureTimeAnticipated = models.NullBooleanField()
	arrivalTimeAnticipated = models.NullBooleanField()

	class Meta:
		managed = False

	def timeForAction(self, action):
		key = action.name.lower()
		return (getattr(self, key + 'Time'), getattr(self, key + 'TimeAnticipated'))

	def update(self, action, time='NoChange', anticipated='NoChange'):
		key = 'departureTime' if action is TrainAction.Departure else 'arrivalTime'
		if time is not 'NoChange':
			self.record.stops[self.index][key] = time
			setattr(self, key, time)
		if anticipated is not 'NoChange':
			key = key + 'Anticipated'
			self.record.stops[self.index][key] = anticipated
			setattr(self, key, anticipated)
		self.record.save()
