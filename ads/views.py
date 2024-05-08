import datetime
import uuid
from rest_framework.viewsets import ModelViewSet, GenericViewSet
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from core.models import Ad
from .serializers import AdsSerializer, AdImageSerializer
from .permissions import IsOwnerOfAd
from .filter import AdsFilter


# Create your views here
class AdViewSets(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOfAd]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdsFilter

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        images = self.request.query_params.get('images')
        queryset = self.queryset
        if images:
            image_ids = self._params_to_ints(images)
            queryset = queryset.filter(images__id__in=image_ids)

        if self.request.user.is_anonymous:
            return queryset.order_by('-id').distinct()

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = self.permission_classes
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return AdImageSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to an ad"""
        ad = self.get_object()
        serializer = AdImageSerializer(data=request.data, context={'ad': ad})

        if serializer.is_valid():
            serializer.save(ad=ad, user=request.user)
            # print(serializer.errors)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Create a new products for a specific authenticated user"""
        serializer.save(user=self.request.user)


class AdsSharableView(mixins.RetrieveModelMixin, GenericAPIView):

    def get(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk)
        sharable_link = ad.generate_sharable_link()
        return JsonResponse({'sharable_link': sharable_link})


def initiate_payment(amount, email, ad_id):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SEC_KEY}"

    }

    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": "http://localhost:8000/ads/payment/confirm_payment/?ad_id=" + ad_id,
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": "080****4528",
            "name": "Yemi Desola"
        },
        "customizations": {
            "title": "Pied Piper Payments",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
        },
        'configurations': {
            'session_duration': 10,  # checkout session timeout
            'max_retry_attempt': 5,  # max payment retries
        }

    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        print("The payment didn't go through!!!")
        return Response({"error": str(err)}, status=500)


class PaymentViewSets(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOfAd]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ad.objects.all()
        return Ad.objects.filter(user=user)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    http_method_names = ["get", "patch", "post", "delete", "options", "head"]

    @action(detail=True, methods=['POST'])
    def pay(self, request, pk):
        ad = self.get_object()
        amount = ad.ad_cost
        email = request.user.email
        ad_id = str(ad.id)
        return initiate_payment(amount, email, ad_id)

    @action(detail=False, methods=["POST"])
    def confirm_payment(self, request):
        ad_id = request.GET.get("ad_id")
        print(ad_id)
        ad = Ad.objects.get(id=ad_id)
        ad.pending_status = "C"
        ad.placed_at = datetime.datetime.now()
        ad.save()
        serializer = AdsSerializer(ad)

        data = {
            "msg": "Payment was successful",
            "data": serializer.data
        }
        return Response(data)
