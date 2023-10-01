from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGEDIENTS_URL='recipe:ingredient-list'

class PublicIngredientApiTest(TestCase):
	def setUp(self):
		self.client=APIClient()

	def test_login_required(self):
		res = self.client.get(INGEDIENTS_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'otra@pavada.com',
			'testpass'
		)
		self.client.force_authenticate(self.user)

	def test_retrieve_ingredient_list(self):
		Ingredient.objects.create(user=self.user, name='leche')
		Ingredient.objects.create(user=self.user, name='queso')

		res = self.client.get(INGEDIENTS_URL)
		ingredients = Ingredient.objects.all().order_by('-name')
		serializer = IngredientSerializer(ingredients, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_ingredients_limited_to_user(self):
		self.user2 = get_user_model().objects.create_user(
			'otra@pavada.com',
			'testpass'
		)
		Ingredient.objects.create(user=self.user2, name='vinegar')
		ingredient = Ingredient.objects.create(user=self.user, name='tumeric')

		res = self.client.get(INGEDIENTS_URL)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, 1)
		self.assertEqual(res.data[0]['name'], ingredient.name)

	def test_create_ingredient_succesful(self):
		payload = {'name':'Chocolate'}
		self.client.post(INGEDIENTS_URL, payload)

		exists = Ingredient.objects.filter(
			user = self.user,
			name=payload['name']
		).exists()

		self.assertTrue(exists)

	def test_create_ingredient_invalid(self):
		payload = {'email': '' }
		res = self.client.post(INGEDIENTS_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)