from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from info.models import Record
from django.contrib.auth import get_user_model


class Trip(models.Model):
	user = models.ForeignKey(get_user_model(), db_index=True, on_delete=models.CASCADE, related_name='trips')
	record = models.ForeignKey(Record, db_index=True, on_delete=models.CASCADE, related_name='trips')
	departureIndex = models.IntegerField()
	arrivalIndex = models.IntegerField()
	seat = models.CharField(max_length=15, null=True)
	boardingGate = models.CharField(max_length=30, null=True)

	relatedTrips = models.ManyToManyField('self')
	nextTrip = models.OneToOneField('self', null=True, on_delete=models.SET_NULL, related_name='previousTrip')


@receiver(pre_delete, sender=Trip, dispatch_uid='TripDeleteMend')
def TripDeleteMend(sender, instance, using, **kwargs):
	if instance.nextTrip is not None:
		instance.previousTrip.nextTrip = instance.nextTrip
