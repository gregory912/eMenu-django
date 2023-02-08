from django_filters import rest_framework as filters
from .models import Menu


class MenuFilter(filters.FilterSet):
    """
    The function accepts fields and indicates how menu table can be filtered
    """
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    created_from = filters.IsoDateTimeFilter(field_name="created", lookup_expr='gte')
    created_up_to = filters.IsoDateTimeFilter(field_name="created", lookup_expr='lte')
    modified_from = filters.IsoDateTimeFilter(field_name="modified", lookup_expr='gte')
    modified_up_to = filters.IsoDateTimeFilter(field_name="modified", lookup_expr='lte')

    class Meta:
        model = Menu
        fields = [
            'name',
            'created',
            'modified',
        ]
