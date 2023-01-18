from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


"""TEST PARA CREAR USUARIOS"""
def create_user(**params):
	"""FUNCION PARA CREAR UN USUARIO AUTOMATICAMENTE"""
	return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
	"""test para clientes web no autenticados"""
	"""definimos el cliente"""
	def setUp(self):
		"""el clente web es un usuario que hace peticiones post"""
		self.client=APIClient()

	def create_valid_user(self):
		"""creacion de un usuario"""
		payload = {
			'email':'test@datadocis.com',
			'password':'testpass',
			'name':'Test Name'
			}
		"""Recibimos un objecto cliente y le asignamos los datos del payload"""
		res = self.client.post(CREATE_USER_URL, payload)
		"""respuesta"""
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		"""CREACION DE UN NUEVO USUARIO"""
		"""llammamos al modelo de usuario, despues a los objetos, y con get obtenemos los datos de usuario de la var res.data para crear un usuario"""
		user = get_user_model().objects.get(**res.data)
		"""le pasamos el objecto self y con hacemos assertTrue comprobacion"""
		"""a la funcion assert le pasamos user y llammamos a check_password"""
		"""le pasamos el diccionario y a su clave -> payload[password]"""
		self.assertTrue(user.check_password(payload['password']))
		self.assertNotIn('password', res.data)

	def test_user_exists(self):
		"""las ** desglosan las caracteristicas del objeto que le pasamos a las funciones"""
		payload={
			'email':'test@datadocis.com',
			'password':'testpass',
			'name':'Test Name'
		}
		create_user(**payload)

		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_password_to_short(self):
		payload = {
			'email':'test@datadocis.com',
			'password':'pw',
			'name':'Test Name'
		}
		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

		user_exists = get_user_model().objects.filter(
			email=payload['email']
		).exists()
		self.assertFalse(user_exists)

	def test_create_token_for_user(self):
		payload = {
			"email":"test@datadocis.com",
			"password":"testpass1234"
		}
		create_user(**payload)
		res = self.client.post(TOKEN_URL, payload)
		print(res.data)
		self.assertIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

	def test_create_token_invalid_credentilas(self):
		create_user(email='test@datadocis.com', password='testpass')
		payload = {'email': 'test@datadocis.com', 'password': 'wrong'}

		res = self.client.post(TOKEN_URL, payload)

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_token_no_user(self):
		payload = {
			'email':'test@datadocis.com',
			'password':'pw',
			'name':'Test Name'
		}
		create_user(**payload)
		res = self.client.post(TOKEN_URL, payload)
		
		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_token_missing_fields(self):
		res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_retrieve_unauthorized(self):
		""" test de autenticacion requerida para el usuario """
		res=self.client.get(ME_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
	def setUp(self):
		"""el clente web es un usuario que hace peticiones post"""
		self.user = create_user(
			email='test@datadocis.com',
			password='testpass',
			name='name',
		)
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
   
	def test_retrieve_profile(self):
		res = self.client.get(ME_URL)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, {
			'name':self.user.name,
			'email':self.user.email,
		})

	def test_post_me_not_allowed(self):
		res = self.client.post(ME_URL, {})
		self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_update_user_profile(self):
		payload = {'name':'new name', 'password':'newpass1234'}
		res = self.client.patch(ME_URL, payload)
		self.user.refresh_from_db()
		self.assertEqual(self.user.name, payload['name'])
		self.assertTrue(self.user.check_password(payload['password']))
		self.assertEqual(res.status_code, status.HTTP_200_OK)


