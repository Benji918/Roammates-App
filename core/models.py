from django.utils import timezone
from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
import uuid
import os
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_rooms, validate_ad_name
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
    AD_PAYMENT_CHOiCES = [
        (5000, 'Duration - 7days'),
        (10000, 'Duration - 14days'),
        (15000, 'Duration - 30days'),
    ]
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    ROOM_AMENITIES_CHOICES = [
        ('water', 'Water'),
        ('furniture', 'Furniture'),
        ('light', 'Light'),
    ]
    AD_TYPE_CHOICES = [
        ('room to rent', 'Room to Rent'),
        ('room wanted', 'Room Wanted'),
        ('whole apartment for rent', 'whole apartment for rent'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    ad_name = models.CharField(max_length=10, blank=False, null=True, unique=True, validators=[validate_ad_name])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_rooms_for_rent = models.IntegerField(blank=False, validators=[validate_rooms])
    size_of_property = models.CharField(max_length=255, blank=False)
    address_of_property = models.URLField(max_length=255, unique=True, blank=False)
    area_of_property = models.CharField(max_length=255, blank=False)
    room_amenities = models.CharField(max_length=255, choices=ROOM_AMENITIES_CHOICES, blank=False)
    cost_of_room = models.IntegerField(blank=False)
    length_of_availability = models.DateField(blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    image = models.ManyToManyField('AdImage', related_name='ads')
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    ad_cost = models.IntegerField(choices=AD_PAYMENT_CHOiCES, blank=False, default=5000)
    ad_type = models.CharField(max_length=255, choices=AD_TYPE_CHOICES, blank=False)
    ad_duration = models.IntegerField(blank=True, null=False, editable=False)
    ad_expiration_date = models.DateTimeField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ad {self.ad_name}"

    def generate_sharable_link(self):
        return f'/ad/{self.id}/sharable-link/'

    def save(self, *args, **kwargs):
        # Calculate ad_duration based on ad_cost
        if not self.ad_duration:
            self.ad_duration = self.calculate_ad_duration(self.ad_cost)

        # Calculate ad_expiration_date based on ad_duration
        if not self.ad_expiration_date:
            self.ad_expiration_date = self.calculate_expiration_date()

        super().save(*args, **kwargs)

    @staticmethod
    def calculate_ad_duration(ad_cost):
        # Example logic to determine ad_duration based on payment ad_cost
        if ad_cost == 5000:
            return 7  # 7 days
        elif ad_cost == 10000:
            return 14  # 14 days
        elif ad_cost == 15000:
            return 30  # 30 days
        else:
            return 0  # Default ad_duration if ad_cost doesn't match any predefined values

    def calculate_expiration_date(self):
        if self.ad_duration:
            return timezone.now() + timezone.timedelta(days=self.ad_duration)
        return None


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


class SavedAd(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='saved_ad')
    saved_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'ad']

    def __str__(self):
        return f'Saved Ad{self.ad.ad_name}'

