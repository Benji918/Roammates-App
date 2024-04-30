from core.models import Ad, AdImage
from rest_framework import serializers


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdsSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, required=False)

    class Meta:
        model = Ad
        fields = ['id', 'no_rooms_for_rent', 'size_of_property', 'address_of_property',
                  'area_of_property', 'room_amenities', 'cost_of_room', 'length_of_availability',
                  'phone_number', 'ad_type', 'images']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def _get_or_create_images(self, images, ad):
        """Helper function for getting or creating images as needed"""
        auth_user = self.context['request'].user
        for image in images:
            img_obj, created = AdImage.objects.get_or_create(
                user=auth_user,
                **image
            )
            Ad.image.add(img_obj)

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        ad = Ad.objects.create(**validated_data)
        self._get_or_create_images(images, ad)
        return ad

    def update(self, instance, validated_data):
        """Update recipe"""
        images = validated_data.pop('images', None)
        if images is not None:
            instance.images.clear()
            self._get_or_create_images(images, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

