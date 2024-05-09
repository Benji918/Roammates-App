from django.contrib import admin
from .models import CustomUser, Ad, AdImage, SavedAd

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ad)
admin.site.register(AdImage)
admin.site.register(SavedAd)

