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

	def to_representation(self, obj):
		data = super(TrainSerializer, self).to_representation(obj)
		for stop in data['stops']:
			station = models.Station.objects.get(id=stop['station'])
			stop['station'] = StationSerializer(station).data

		return data


class RecordSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Record
		fields = ('id', 'departureDate', 'train', 'stops')
