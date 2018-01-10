import hashlib
from rest_framework import serializers
from allauth.account.models import EmailAddress
from allauth.account import signals
from rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer


class EmailSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmailAddress
		fields = ('id', 'email', 'verified', 'primary')

	def validate_primary(self, value):
		if value is False:
			return value

		if not self.instance.verified and EmailAddress.objects.filter(user=self.context['request'].user, verified=True).exists():
			raise serializers.ValidationError('The requested email address is not verified.')

		return value

	def create(self, validated_data):
		request = self.context['request']
		return EmailAddress.objects.add_email(request, request.user, validated_data["email"], confirm=True)

	def update(self, instance, validated_data):
		request = self.context['request']
		if validated_data.get('verified'):
			instance.send_confirmation(request)
		if validated_data.get('primary'):
			from_email_address = EmailAddress.objects.filter(user=request.user, primary=True).first()
			instance.set_as_primary()
			signals.email_changed.send(sender=request.user.__class__, request=request, user=request.user, from_email_address=from_email_address, to_email_address=instance)
		return instance


class UserDetailsSerializer(DefaultUserDetailsSerializer):
	hash = serializers.SerializerMethodField()

	def get_hash(self, user):
		return hashlib.md5(user.email.lower().encode()).hexdigest()

	class Meta(DefaultUserDetailsSerializer.Meta):
		fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'hash')
