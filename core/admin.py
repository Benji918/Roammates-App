from django.contrib import admin
from .models import CustomUser, Ad, AdImage, AdPayment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ad)
admin.site.register(AdImage)
admin.site.register(AdPayment)
