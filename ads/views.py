from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Ad
from .serializers import AdsSerializer
from .permissions import IsOwnerOfAd


# Create your views here
class AdViewSets(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOfAd]

    def get_queryset(self):
        """Return only lodge objects for the request user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return AdsSerializer
        return self.serializer_class

    @action(methods=['POST', 'PUT', 'DELETE'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image for a lodge object"""
        lodge = self.get_object()
        serializer = self.get_serializer(lodge, data=request.data)

        if serializer.is_valid():
            serializer.save()
            # Return the appropriate status code based on the HTTP method
            if request.method == 'POST':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif request.method == 'PUT':
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'DELETE':
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_name='sharable-link', url_path='sharable-link')
    def get_sharable_link(self, request, pk=None):
        """Get the sharable link for a product"""
        ad = self.get_object()
        sharable_link = request.build_absolute_uri(reverse('ad-detail', args=[ad.id]))
        return Response({'sharable_link': sharable_link})

    def perform_create(self, serializer):
        """Create a new products for a specific authenticated user"""
        serializer.save(user=self.request.user)
