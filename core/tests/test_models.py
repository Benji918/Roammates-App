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


    def test_create_ad(self):
        """Test creating an ad"""
        user = create_user()
        ad = models.Ad.objects.create(
            ad_name='Test Ad',
            user=user,
            no_rooms_for_rent=3,
            size_of_property='Medium',
            address_of_property='123 Test St',
            area_of_property='Test Area',
            room_amenities='water',
            cost_of_room=5000,
            phone_number='1234567890',
            ad_type='room to rent',
            length_of_availability='2024-09-12',
        )

        self.assertEqual(ad.ad_name, 'Test Ad')
        self.assertEqual(ad.user, user)
        self.assertEqual(ad.no_rooms_for_rent, 3)
        self.assertEqual(ad.size_of_property, 'Medium')
        self.assertEqual(ad.address_of_property, '123 Test St')
        self.assertEqual(ad.area_of_property, 'Test Area')
        self.assertEqual(ad.room_amenities, 'water')
        self.assertEqual(ad.cost_of_room, 5000)
        self.assertEqual(ad.phone_number, '1234567890')
        self.assertEqual(ad.ad_type, 'room to rent')
        self.assertIsNotNone(ad.ad_duration)
        self.assertIsNotNone(ad.ad_expiration_date)

    def test_create_adimage(self):
        """Test creating an ad image"""
        user = create_user()
        ad = models.Ad.objects.create(
            ad_name='Test Ad',
            user=user,
            no_rooms_for_rent=3,
            size_of_property='Medium',
            address_of_property='123 Test St',
            area_of_property='Test Area',
            room_amenities='water',
            cost_of_room=5000,
            phone_number='1234567890',
            ad_type='room to rent',
            length_of_availability = '2024-09-12',
        )
        ad_image = models.AdImage.objects.create(
            user=user,
            ad=ad,
            image='Screenshot 2024-03-07 091812.png'  # Replace 'test.jpg' with the path to an actual image file
        )

        self.assertEqual(ad_image.user, user)
        self.assertEqual(ad_image.ad, ad)
        self.assertEqual(ad_image.image, 'Screenshot 2024-03-07 091812.png')
