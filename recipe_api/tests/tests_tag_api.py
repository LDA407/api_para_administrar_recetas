from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerialiser


TAG_URL = 'recipe:tag-list'
# Create your tests here.
class PublicTagsApiTest(TestCase):
	"""PROBAR LOS API TAG DISPONIBLES PUBLICAMENTE"""
	def setUp(self):
		self.client=APIClient()

	def tag_login_required(self):
		res = self.client.get(TAG_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user('test@dosis.com', 'testpass')
		self.client=APIClient()
		self.client.force_authenticate(self.user)

	def test_retrieve_tags(self):
		Tag.objects.create(user=self.user, name='Testname')
		Tag.objects.create(user=self.user, name='Banana')

		res = self.client.get(TAG_URL)
		tags = Tag.objects.all().order_by('-name')

		serializer = TagSerialiser(tags, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_tag_limited_to_user(self):
		user2 = get_user_model().objects.create_user('otra@pavada.com', 'testpass')
		Tag.objects.create(user=user2, name='raspberry')
		tag = Tag.objects.create(user=self.user, name='confort food')

		res = self.client.get(TAG_URL)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data[0]['name'], tag.name)

	def test_create_tag_successful(self):
		payload = {'name':'nkljmlk'}
		self.client.post(TAG_URL, payload)

		exists = Tag.objects.filter(
			user = self.user,
			name=payload['name']
		).exists()

		self.assertTrue(exists)

	def test_crated_tag_invalid(self):
		payload = {'name': ''}
		res = self.client.post(TAG_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)