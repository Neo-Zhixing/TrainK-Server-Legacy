from train import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Station
		fields = ('name', 'telecode', 'id')


class TrainSerializer(serializers.ModelSerializer):
	serializeStops = True

	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		self.serializeStops = kwargs.pop('stops', True)
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
			del data['stops']
			stopsToSerialize = [data['originStop'], data['destinationStop']]

		for stop in stopsToSerialize:
			station = models.Station.objects.get(id=stop['station'])
			stop['station'] = StationSerializer(station).data

		return data


class RecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Record
		fields = ('departureDate', 'stops')
