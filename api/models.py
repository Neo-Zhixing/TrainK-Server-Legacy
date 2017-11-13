from django.db import models
from django.contrib.postgres import fields
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta
import re


class Station(models.Model):
	name = models.CharField(max_length=10)
	telecode = models.CharField(max_length=5, blank=True)


class Train(models.Model):
	names = fields.ArrayField(models.CharField(max_length=10))
	telecode = models.CharField(max_length=50)
	stops = fields.JSONField(encoder=DjangoJSONEncoder)

	@property
	def name(self):
		nameStr = ''
		for name in self.names:
			nameStr += name + '/'
		return nameStr[:-1]

	@classmethod
	def from_db(cls, db, field_names, values):
		instance = super(Train, cls).from_db(db, field_names, values)

		def convertStop(stop):
			for key in ['departureTime', 'arrivalTime']:
				if not stop[key]:
					continue
				(sign, days, hours, minutes, seconds, ms) = re.match(r'^(-?)P(\d+)DT(\d{2})H(\d{2})M(\d{2}).?(\d{6})?S$', stop[key]).groups()
				if not ms:
					ms = 0

				stop[key] = timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(ms))
				if sign == '-':
					stop[key] = -stop[key]
			return stop

		instance.stops = [convertStop(stop) for stop in instance.stops]
		return instance


class Record(models.Model):
	departureDate = models.DateField()
	train = models.ForeignKey(Train)
	stops = fields.JSONField(encoder=DjangoJSONEncoder)
