from core.models import Ad, AdImage, SavedAd, RoomAmenity
from rest_framework import serializers, fields

from django.core.exceptions import ValidationError


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Validate the image count
        ad = self.context.get('ad')  # Assuming ad is passed in the serializer context
        if ad.images.count() >= 10:
            raise ValidationError("An ad can only have a maximum of 10 images.")

        # Validate the image file extension and size
        image = data.get('image')
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("Only JPG, JPEG, and PNG images are allowed.")

            if image.size > 1024 * 1024:  # 1MB limit
                raise ValidationError("Image size should not exceed 1MB.")

        return data


class AdsSerializer(serializers.ModelSerializer):
    images = AdImageSerializer(many=True, required=False)
    room_amenities = fields.MultipleChoiceField(choices=Ad.ROOM_AMENITIES_CHOICES)

    class Meta:
        model = Ad
        fields = ['id', 'ad_name', 'no_rooms_for_rent', 'size_of_property', 'address_of_property',
                  'area_of_property', 'cost_of_room', 'length_of_availability',
                  'phone_number', 'ad_type', 'ad_cost', 'room_amenities', 'images']
        read_only_fields = ['id', 'created_at', 'updated_at']

    # def validate(self, data):
    #     """Convert room_amenities between list and string formats"""
    #     room_amenities = data.get('room_amenities')
    #
    #     # If room_amenities is a list, convert it to a comma-separated string
    #     if isinstance(room_amenities, list):
    #         data['room_amenities'] = ','.join(room_amenities)
    #     # If room_amenities is a string, split it into a list
    #     elif isinstance(room_amenities, str):
    #         data['room_amenities'] = room_amenities.split(',')
    #
    #     return data

    def _get_or_create_images(self, images, ad):
        """Helper function for getting or creating images as needed"""
        auth_user = self.context.get('request').user
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


class SavedAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAd
        fields = ['id']
        read_only_fields = ['id']
