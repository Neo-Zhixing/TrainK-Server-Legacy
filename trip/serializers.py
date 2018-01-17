from .models import Trip
from info.models import Record
from info.serializers import RecordSerializer
from rest_framework import serializers


class TripSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	record = RecordSerializer(unnest=False, read_only=True)
	recordId = serializers.PrimaryKeyRelatedField(source='record', queryset=Record.objects, write_only=True)

	class Meta:
		model = Trip
		fields = ('id', 'user', 'record', 'recordId', 'departureIndex', 'arrivalIndex', 'seat', 'boardingGate')
