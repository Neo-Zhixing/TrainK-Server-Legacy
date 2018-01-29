from django.db import models
from django.conf import settings


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cr_profile')
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50, null=True)
