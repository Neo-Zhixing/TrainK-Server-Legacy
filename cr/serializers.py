from . import models
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	password_info = serializers.SerializerMethodField(read_only=True)
	password = serializers.CharField(max_length=50, write_only=True)

	class Meta:
		model = models.Profile
		fields = ('user', 'username', 'password', 'password_info')

	def get_password_info(self, obj):
		return None if obj.password is None else len(obj.password)
