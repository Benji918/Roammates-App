from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AdViewSets, AdsSharableView, PaymentViewSets, SavedAdViewSet

router = DefaultRouter()
router.register('', AdViewSets)
router.register('payment', PaymentViewSets, basename='payment')
router.register('', SavedAdViewSet, basename='save-ads')

app_name = 'ads'

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:pk>/sharable-link/', AdsSharableView.as_view()),


]
