from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Ad, AdImage
from .serializers import AdsSerializer, AdImageSerializer
from .permissions import IsOwnerOfAd
from rest_framework import views


# Create your views here
class AdViewSets(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOfAd]

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
        ad = self.get_object()
        serializer.save(ad=ad, user=self.request.user)


class AdsSharableView(mixins.RetrieveModelMixin, GenericAPIView):

    def get(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk)
        sharable_link = ad.generate_sharable_link()
        return JsonResponse({'sharable_link': sharable_link})
