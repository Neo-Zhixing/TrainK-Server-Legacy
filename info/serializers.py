from . import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Station
		fields = ('name', 'telecode', 'id')


class TrainSerializer(serializers.ModelSerializer):

	def __init__(self, *args, **kwargs):
		self.serializeStops = kwargs.pop('serializeStops', True)
		self.stopsToInclude = kwargs.pop('includingStops', {})
		super(TrainSerializer, self).__init__(*args, **kwargs)

	class Meta:
		model = models.Train
		fields = ('names', 'telecode', 'stops')

	def to_representation(self, obj):
		data = super(TrainSerializer, self).to_representation(obj)

		if self.serializeStops:
			stopsToSerialize = data['stops']
		else:
			data['originStop'] = data['stops'][0]
			data['destinationStop'] = data['stops'][-1]
			stopsToSerialize = [data['originStop'], data['destinationStop']]

			additionalStops = dict((self.stopsToInclude[stop['station']], stop) for stop in data['stops'] if stop['station'] in self.stopsToInclude)
			data.update(additionalStops)
			stopsToSerialize += additionalStops.values()

			del data['stops']

		for stop in stopsToSerialize:
			if isinstance(stop['station'], int):
				station = models.Station.objects.get(id=stop['station'])
				stop['station'] = StationSerializer(station).data

		return data


class RecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Record
		fields = ('departureDate', 'stops')
