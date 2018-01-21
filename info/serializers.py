from . import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Station
		fields = ('name', 'telecode', 'id', 'abbreviation', 'spell')


def _unnest_stop(stop):
	if isinstance(stop['station'], int):
		station = models.Station.objects.get(id=stop['station'])
		stop['station'] = StationSerializer(station).data
	return stop


def _get_stop(train, index):
	if not train.stops:
		return None
	return _unnest_stop(train.stops[index])


class TrainListSerializer(serializers.ModelSerializer):
	origin = serializers.SerializerMethodField()
	destination = serializers.SerializerMethodField()

	def get_origin(self, train):
		return _get_stop(train, 0)

	def get_destination(self, train):
		return _get_stop(train, -1)

	class Meta:
		model = models.Train
		fields = ('names', 'telecode', 'since', 'origin', 'destination')


class TrainDetailSerializer(serializers.ModelSerializer):
	stops = serializers.SerializerMethodField()

	def get_stops(self, train):
		return [_unnest_stop(stop) for stop in train.stops] if train.stops else None

	class Meta:
		model = models.Train
		fields = ('names', 'telecode', 'since', 'stops')


class RecordListSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Record
		fields = ('id', 'departureDate', 'train', 'delay')


class RecordSerializer(RecordListSerializer):
	train = TrainListSerializer()

	class Meta(RecordListSerializer.Meta):
		pass


class RecordDetailSerializer(RecordListSerializer):
	train = TrainDetailSerializer()

	class Meta(RecordListSerializer.Meta):
		fields = ('id', 'departureDate', 'train', 'delay', 'stops')
