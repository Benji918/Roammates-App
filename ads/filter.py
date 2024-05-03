import django_filters
from core.models import Ad


class AdsFilter(django_filters.FilterSet):
    ORDER_CHOICES = (
        ('newest', 'Newest Ads'),
        ('last_updated', 'Last Updated'),
        ('lowest_price', 'Lowest Price First'),
        ('highest_price', 'Highest Price First'),
    )
    order_by = django_filters.ChoiceFilter(label='Order By', choices=ORDER_CHOICES, method='filter_order')

    def filter_order(self, queryset, name, value):
        if value == 'newest':
            return queryset.order_by('-created_at')
        elif value == 'last_updated':
            return queryset.order_by('-updated_at')
        elif value == 'lowest_price':
            return queryset.order_by('cost_of_room')
        elif value == 'highest_price':
            return queryset.order_by('-cost_of_room')
        return queryset

    class Meta:
        model = Ad
        fields = []
