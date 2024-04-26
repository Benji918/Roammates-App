from core.models import Ad, CustomUser
from rest_framework import serializers


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'no_rooms_for_rent', 'size_of_property', 'address_of_property',
                  'area_of_property', 'room_amenities', 'cost_of_room', 'length_of_availability',
                  'phone_number', 'ad_type', 'ad_image']
        read_only_fields = ['id', 'created_at', 'updated_at']
