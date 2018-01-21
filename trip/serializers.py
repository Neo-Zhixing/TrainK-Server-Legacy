from .models import Trip
from info.models import Record
from info.serializers import RecordSerializer, _unnest_stop
from rest_framework import serializers


class TripSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	record = RecordSerializer(read_only=True)
	recordId = serializers.PrimaryKeyRelatedField(source='record', queryset=Record.objects, write_only=True)

	departure = serializers.SerializerMethodField(read_only=True)
	arrival = serializers.SerializerMethodField(read_only=True)

	def get_departure(self, trip):
		return _unnest_stop(trip.record.train.stops[trip.departureIndex]) if trip.record.train.stops else None

	def get_arrival(self, trip):
		return _unnest_stop(trip.record.train.stops[trip.arrivalIndex]) if trip.record.train.stops else None

	class Meta:
		model = Trip
		fields = ('id', 'user', 'record', 'recordId', 'departure', 'arrival', 'departureIndex', 'arrivalIndex', 'seat', 'boardingGate')
