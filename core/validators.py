from django.core.exceptions import ValidationError


def validate_rooms(value):
    if not isinstance(value, int):
        raise ValidationError('Number of rooms must be an integer')
    if value < 1 or value > 100:
        raise ValidationError('Number of rooms must be between 1 and 100')


def validate_ad_name(data):
    if len(data) <= 5:
        raise ValidationError('Ad name must be more than 5 characters!')
