from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer, TagSerializer
import os
from PIL import Image


RECIPES_URL = 'recipe:recipe-list'


# Create your tests here.
def sample_tag(user, name='Main course'):
	return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='Cinnamon'):
	return Ingredient.objects.create(user=user, name=name)

def detail_url(recipe_id):
	return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_recipe(user, **params):
	defaults = {
		'title' : 'sample recipe',
		'time_minutes' : 10,
		'price' : 5.00,
	}
	defaults.update(params)

	return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):
	"""PROBAR LOS API TAG DISPONIBLES PUBLICAMENTE"""
	def setUp(self):
		self.client=APIClient()
		self.user = get_user_model().objects.create_user(
			'test@testrecipe.com',
			'1234test'
		)
		self.client.force_authenticate(user=self.user)

	def test_retrieve_recipe(self):
		sample_recipe(user=self.user)
		sample_recipe(user=self.user)

		res = self.client.get(RECIPES_URL)

		recipes = Recipe.objects.all().order_by('id')
		serializer = RecipeSerializer(recipes, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_recipe_limited_to_user(self):
		user2 = get_user_model().objects.create_user('otra@pavada.com', 'testpass')

		sample_recipe(user=self.user2)
		sample_recipe(user=self.user)

		res = self.client.get(RECIPES_URL)

		recipes = Recipe.objects.filter(user=self.user)
		serializer = RecipeSerializer(recipes, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data, serializer.data)

	def test_view_recipe_detail(self):
		recipe = sample_recipe(user=self.user)
		recipe.Tag.add(sample_tag(user=self.user))
		recipe.Ingredient.add(sample_ingredient(user=self.user))

		url=detail_url(recipe.id)
		res = self.client.get(url)

		serializer = RecipeDetailSerializer(recipe)
		self.assertEqual(res.data, serializer.data)

	def test_create_basic_recipe(self):
		payload = {
			'title' : 'sample recipe',
			'time_minutes' : 10,
			'price' : 59.00,
			}

		res = self.client.post(RECIPES_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id'])
		for key in payload.keys():
			self.assertEqual(payload[key], getattr(recipe, key))

	def test_create_recipe_with_tags(self):
		tag1 = sample_tag(user=self.user, name='tag 1')
		tag2 = sample_tag(user=self.user, name='tag 2')
		payload = {
			'title' : 'sample recipe',
			'tags' : [tag1.id ,tag2.id],
			'time_minutes' : 10,
			'price' : 59.00,
		}
		res = self.client.post(RECIPES_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id'])
		tags = recipe.tags.all()
		self.assertEqual(tags.count(), 2)
		self.assertIn(tag1, tags)
		self.assertIn(tag2, tags)

	def test_create_recipe_with_ingredients(self):
		ingredient1 = sample_tag(user=self.user, name='Ingredient 1')
		ingredient2 = sample_tag(user=self.user, name='Ingredient 2')
		payload = {
			'title' : 'sample recipe',
			'tags' : [ingredient1.id ,ingredient2.id],
			'time_minutes' : 10,
			'price' : 59.00,
		}
		res = self.client.post(RECIPES_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id'])
		ingredients = recipe.ingredients.all()
		self.assertEqual(ingredients.count(), 2)
		self.assertIn(ingredient1, ingredients)
		self.assertIn(ingredient2, ingredients)


class PrivateRecipeApiTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user('test@dosis.com', 'testpass')
		self.client=APIClient()
		self.client.force_authenticate(self.user)

	