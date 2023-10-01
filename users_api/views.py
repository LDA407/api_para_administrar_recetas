from user.serializers import UserSerializers, AuthTokenSerializers
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings



# Create your views here.
class CreateUserView(generics.CreateAPIView):
	serializer_class = UserSerializers

class CreateTokenView(ObtainAuthToken):
	serializers_class = AuthTokenSerializers
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManagerUserView(generics.RetrieveUpdateAPIView):
	serializer_class = UserSerializers
	authentication_classes = (authentication.TokenAuthentication,)
	permissions_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		""" Obtener y retornar un usuario autenticado """
		return self.request.user