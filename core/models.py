from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
import uuid
import os
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_rooms
from django.utils.translation import gettext_lazy as _


def ad_image_file(instance, filename):
    """Generate filename for new object image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'ad', filename)


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    username = models.CharField(unique=True, max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    paid_for_ad = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Ad(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_rooms_for_rent = models.IntegerField(blank=False, validators=[validate_rooms])
    size_of_property = models.CharField(max_length=255, blank=False)
    address_of_property = models.CharField(max_length=255, unique=True, blank=False)
    area_of_property = models.CharField(max_length=255, blank=False)
    ROOM_AMENITIES_CHOICES = [
        ('water', 'Water'),
        ('furniture', 'Furniture'),
        ('light', 'Light'),
    ]
    room_amenities = models.CharField(max_length=255, choices=ROOM_AMENITIES_CHOICES, blank=False)
    cost_of_room = models.IntegerField(blank=False)
    length_of_availability = models.DateField(blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    AD_TYPE_CHOICES = [
        ('room to rent', 'Room to Rent'),
        ('room wanted', 'Room Wanted'),
        ('whole apartment for rent', 'whole apartment for rent'),
    ]
    image = models.ManyToManyField('AdImage', related_name='ads')
    ad_type = models.CharField(max_length=255, choices=AD_TYPE_CHOICES, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ad {self.address_of_property}"

    def generate_sharable_link(self):
        return f'/ad/{self.id}/sharable-link/'


class AdImage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=False, blank=False, upload_to=ad_image_file)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for Ad {self.id}"


class AdPayment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad-payment')

    def __str__(self):
        return f'Ad payment -> {self.pending_status}'

