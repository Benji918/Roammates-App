from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


def create_user(**params):
    """Create and return a user"""
    default = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    default.update(params)
    user = get_user_model().objects.create_user(**default)
    return user


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating user with email successfully"""
        email = 'test@example.com'
        password = '123456789'
        user = create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))



    def test_create_new_user_without_an_email(self):
        """Creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            create_user(email='', password='123456789')

    def test_create_superuser(self):
        """Test creation of superuser"""
        email = 'test@example.com'
        password = '123456789'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
