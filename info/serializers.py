from . import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Station
		fields = ('name', 'telecode', 'id', 'abbreviation', 'spell')


class TrainSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Train
		fields = ('names', 'telecode', 'stops')


class RecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Record
		fields = ('departureDate', 'stops')
