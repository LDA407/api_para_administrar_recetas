from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient, Recipe
from recipe_api import serializers


# Create your views here.
class BaseRecipeAttrsViewSet(
		viewsets.GenericViewSet,
		mixins.ListModelMixin,
		mixins.CreateModelMixin
	):
	authentication_class = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		return self.queryset.filter(user=self.request.user).order_by('-name')

	def perform_create(self, serializers):
		serializers.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrsViewSet):
	queryset = Tag.objects.all()
	serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrsViewSet):
	queryset = Ingredient.objects.all()
	serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.RecipeSerializer
	queryset = Recipe.objects.all()
	# authentication_class = (TokenAuthentication,)
	# permissions_classes = (IsAuthenticated,)

	# def get_queryset(self):
	# 	return self.queryset.filter(user=self.request.user)

	def get_serializer_class(self):
		if self.action == 'retrieve':
			return serializers.RecipeDetailSerializer

		return self.serializer_class

	def perform_create(self, serializers):
		serializers.save(user=self.request.user)
