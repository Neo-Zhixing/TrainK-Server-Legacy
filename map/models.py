from django.db import models
from info.models import Station as OriginStation


class Station(models.Model):
	station = models.OneToOneField(OriginStation, on_delete=models.CASCADE)
	x = models.FloatField()
	y = models.FloatField()
	latitude = models.FloatField()
	longitude = models.FloatField()
