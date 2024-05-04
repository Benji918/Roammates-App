from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer
from django.core.exceptions import ValidationError


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']

    def validate(self, value):
        if len(value) < 5:
            raise ValidationError('The username must be at least 5 characters long.')



class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'username']
