from django.core.exceptions import ValidationError


def validate_rooms(value):
    if not isinstance(value, int):
        raise ValidationError('Number of rooms must be an integer')
    if value < 1 or value > 100:
        raise ValidationError('Number of rooms must be between 1 and 100')

