from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email='test@datadosis.com', password='testpass'):
	return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_created_user_with_email(self):
        """test para crear un nuevo usuario"""
        email = 'test@datadosis.com'
        password = 'testpass1234'

        user=get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        email = 'test@DATADOSIS.COM'
        user = get_user_model().objects.create_user(email,'testpass1234')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass1234')

    def test_create_new_superuser(self):
        """chekear el superusuario"""
        email = 'test@datadosis.com'
        password = 'testpass1234'
        user=get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tags_str(self):
        tag=models.Tag.objects.create(
            user=sample_user(),
            name='milk'
            )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name = 'Banana'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='wmjoimdomd',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        uuid = 'test_uuid'
        mock_uuid.return_value=uuid
        file_path= models.recipe_image_file_path(None, 'img.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
