from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializers(serializers.ModelSerializer):
	class Meta():
		model = get_user_model()
		fields = ('email', 'username' ,'password')
		extra_kwargs = {'password':{'write_only':True, 'min_length': 5,}}

	def create(self, validated_data):
		return get_user_model().objects.create_user(**validated_data)

	def update(self, instance, validated_data):
		""" Actualizo el usuario y configuro la contraseña para retornalos """
		password = validated_data.pop('password', None)
		user = super().update(instance, validated_data)

		if password:
			user.set_password(password)
			user.save()

		return user


class AuthTokenSerializers(serializers.Serializer):
	"""autenticador para el objeto usuario"""
	email = serializers.CharField()
	username = serializers.CharField()
	password = serializers.CharField(
		style = {'input_type': 'password'}, 
		trim_whitespace = False
	) 

	def validate(self, attrs):
		username=attrs.get('username')
		email=attrs.get('email')
		password=attrs.get('password')

		user=authenticate(
			request = self.context.get('request'),
			username = username,
			email = email,
			password = password 
		)
		if not user:
			msg = _('Unable to authenticate with provider credentials')
			raise serializers.ValidationError(msg, code='authorization')

		attrs['user'] = user
		return attrs


