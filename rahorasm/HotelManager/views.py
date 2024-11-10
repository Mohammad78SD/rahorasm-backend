from rest_framework import generics
from.models import Hotel
from.serializers import HotelSerializer
from django_filters.rest_framework import DjangoFilterBackend


class HotelDetails(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    
class HotelList(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'city__name': ['exact'],
        'city__country__name': ['exact'],
        'city__country__continent__name': ['exact'],
    }
    
    def get_queryset(self):
        queryset = super().get_queryset()
        city_name = self.request.query_params.get('city', None)
        country_name = self.request.query_params.get('country', None)
        continent_name = self.request.query_params.get('continent', None)
        if city_name is not None:
            queryset = queryset.filter(city__name=city_name)
        if country_name is not None:
            queryset = queryset.filter(city__country__name=country_name)
        if continent_name is not None:
            queryset = queryset.filter(city__country__continent__name=continent_name)
        return queryset