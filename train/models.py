from django.db import models
from django.contrib.postgres import fields
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_duration
from django.utils.duration import _get_duration_components as durationComponents
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

	def stop(self, index):
		return Stop(jsonData=self.stops[index])

	@property
	def allStops(self):
		for stop in self.stops:
			yield Stop(jsonData=stop)

	@property
	def originStop(self):
		return Stop(jsonData=self.stops[0])

	@property
	def destinationStop(self):
		return Stop(jsonData=self.stops[-1])


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

	def timeComponents(self, action):
		time = self.departureTime if action is TrainAction.Departure else self.arrivalTime
		if time is None:
			return None
		key = '_timeComponents' + action.name
		if hasattr(self, key):
			return getattr(self, key)
		components = {}
		days, hours, minutes, _, _ = durationComponents(time)
		components['formatted'] = "{:02d}:{:02d}".format(hours, minutes)
		components['days'] = days
		components['hours'] = hours
		components['minutes'] = minutes
		setattr(self, key, components)
		return components

	@property
	def departureTimeComponents(self):
		return self.timeComponents(TrainAction.Departure)

	@property
	def arrivalTimeComponents(self):
		return self.timeComponents(TrainAction.Arrival)

	def __init__(self, jsonData):
		super(Stop, self).__init__()
		self.index = jsonData.get('index')
		self.departureTimeAnticipated = jsonData.get('departureTimeAnticipated')
		self.arrivalTimeAnticipated = jsonData.get('arrivalTimeAnticipated')

		departureTime = jsonData.get('departureTime')
		if departureTime:
			self.departureTime = parse_duration(departureTime)

		arrivalTime = jsonData.get('arrivalTime')
		if arrivalTime:
			self.arrivalTime = parse_duration(arrivalTime)

		stationID = jsonData.get('station')
		if stationID:
			self.station = Station.objects.get(id=stationID)

	class Meta:
		managed = False

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


class TrainAction(enum.Enum):
		Departure = 1
		Arrival = 0
