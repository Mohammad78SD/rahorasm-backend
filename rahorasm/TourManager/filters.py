from django_filters import rest_framework as filters
from .models import City, Country, AirLine, Airport, Tour

class CityFilter(filters.FilterSet):
    class Meta:
        model = City
        fields = {
            'name': ['exact', 'icontains'],  # Filter by exact match or case-insensitive containment
        }

class CountryFilter(filters.FilterSet):
    class Meta:
        model = Country
        fields = {
            'name': ['exact', 'icontains'],
        }

class AirLineFilter(filters.FilterSet):
    class Meta:
        model = AirLine
        fields = {
            'name': ['exact', 'icontains'],
        }

class AirportFilter(filters.FilterSet):
    class Meta:
        model = Airport
        fields = {
            'name': ['exact', 'icontains'],
            'short_name': ['exact', 'icontains'],
            # 'city': ['exact'],  # Filter by city ID
        }


class TourFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')  # Case-insensitive contains
    price = filters.NumberFilter(field_name='least_price', lookup_expr='exact')  # Exact match
    price_gt = filters.NumberFilter(field_name='least_price', lookup_expr='gt')  # Greater than
    price_lt = filters.NumberFilter(field_name='least_price', lookup_expr='lt')  # Less than
    price_gte = filters.NumberFilter(field_name='least_price', lookup_expr='gte')  # Greater than or equal to
    price_lte = filters.NumberFilter(field_name='least_price', lookup_expr='lte')  # Less than or equal to
    tour_type = filters.ChoiceFilter(field_name='tour_type')  # Filter by tour type

    class Meta:
        model = Tour
        fields = {
            'title': ['exact', 'icontains'],
            'tour_type': ['exact'],  # Can also use ChoiceFilter for predefined choices
            'created_at': ['exact', 'year__gt', 'year__lt'],  # Created date filters
            'edited_at': ['exact', 'year__gt', 'year__lt'],  # Edited date filters
            'least_price': ['exact', 'gt', 'lt', 'gte', 'lte'],  # Price filters
        }