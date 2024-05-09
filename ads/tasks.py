from celery import shared_task
from django.utils import timezone
from core.models import Ad

@shared_task
def delete_expired_ads():
    # Get all expired ads
    expired_ads = Ad.objects.filter(ad_expiration_date__lte=timezone.now())

    # Delete expired ads
    expired_ads.delete()
