from . import models
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = models.Profile
		fields = ('user', 'username', 'password')
