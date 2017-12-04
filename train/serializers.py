from train import models
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Station
		fields = ('name', 'telecode')
