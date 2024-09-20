from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Country, AirLine, Airport, Package, Tour
from .serializers import (
    CitySerializer,
    CountrySerializer,
    AirLineSerializer,
    AirportSerializer,
    PackageSerializer,
    TourSerializer,
)
from .filters import (
    CityFilter,
    CountryFilter,
    AirLineFilter,
    AirportFilter,
    PackageFilter,
    TourFilter,
)

class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CityFilter

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CountryFilter

class AirLineListView(generics.ListAPIView):
    queryset = AirLine.objects.all()
    serializer_class = AirLineSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AirLineFilter

class AirportListView(generics.ListAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AirportFilter

class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackageFilter

class TourListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter
    