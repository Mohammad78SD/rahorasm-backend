from django_filters import rest_framework as filters
from .models import City, Country, AirLine, Airport, Package, Tour

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

class PackageFilter(filters.FilterSet):
    class Meta:
        model = Package
        fields = {
            'title': ['exact', 'icontains'],
            # 'city': ['exact'],  # Filter by city ID
            # 'country': ['exact'],  # Filter by country ID
        }

class TourFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')  # Case-insensitive contains
    price = filters.NumberFilter(field_name='price', lookup_expr='exact')  # Exact match
    price_gt = filters.NumberFilter(field_name='price', lookup_expr='gt')  # Greater than
    price_lt = filters.NumberFilter(field_name='price', lookup_expr='lt')  # Less than
    price_gte = filters.NumberFilter(field_name='price', lookup_expr='gte')  # Greater than or equal to
    price_lte = filters.NumberFilter(field_name='price', lookup_expr='lte')  # Less than or equal to
    tour_type = filters.ChoiceFilter(field_name='tour_type')  # Filter by tour type
    package = filters.NumberFilter(field_name='package')  # Filter by package ID
    start_date = filters.DateFilter(field_name='start_date')  # Exact match for start date
    end_date = filters.DateFilter(field_name='end_date')  # Exact match for end date

    class Meta:
        model = Tour
        fields = {
            'title': ['exact', 'icontains'],
            'tour_type': ['exact'],  # Can also use ChoiceFilter for predefined choices
            'package': ['exact'],  # Foreign key filter
            'start_date': ['exact', 'year__gt', 'year__lt'],  # Date filters
            'end_date': ['exact', 'year__gt', 'year__lt'],  # Date filters
            'created_at': ['exact', 'year__gt', 'year__lt'],  # Created date filters
            'edited_at': ['exact', 'year__gt', 'year__lt'],  # Edited date filters
            'price': ['exact', 'gt', 'lt', 'gte', 'lte'],  # Price filters
        }