from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AdViewSets, AdsSharableView

router = DefaultRouter()
router.register('', AdViewSets)

app_name = 'ads'

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:pk>/sharable-link/', AdsSharableView.as_view()),

]
