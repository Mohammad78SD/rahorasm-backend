from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import OuterRef, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Country, AirLine, Airport, Package, Tour, Continent
from VisaManager.models import Visa
from VisaManager.serializers import VisaSerializer
from .serializers import (
    CitySerializer,
    CountrySerializer,
    AirLineSerializer,
    AirportSerializer,
    PackageSerializer,
    TourSerializer,
    ContinentSerializer,
    NavbarCitySerializer,
    NavbarContinentSerializer,
    NavbarCountrySerializer
)
from .filters import (
    CityFilter,
    CountryFilter,
    AirLineFilter,
    AirportFilter,
    PackageFilter,
    TourFilter,
)
from rest_framework.filters import OrderingFilter

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
    serializer_class = PackageSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        queryset = Package.objects.all().prefetch_related('tours')
        continent_id = self.request.query_params.get('continent', None)
        countery_id = self.request.query_params.get('countery', None)
        city_id = self.request.query_params.get('city', None)
        if countery_id:
            queryset.filter(tours__city__counteris__id=countery_id)

        if continent_id:
            queryset.filter(tours__city__counnteris__continents__id=continent_id)
        if countery_id:
            queryset.filter(tours__city__countery__id=countery_id)
        if city_id:
            queryset.filter(tour_city__id=city_id)

        return queryset

    filterset_fields = {
        'city': ['exact'],
        # 'country': ['exact'],
        'created_at': ['gte', 'lte'],
        # Add more filters as needed
    }

    ordering_fields = ['created_at', 'tours__price', 'tours__start_date']  # Allow ordering by tour fields
    ordering = ['created_at']  # Default ordering

class TourListView(generics.ListAPIView):
    serializer_class = TourSerializer
    def get_queryset(self):
        queryset = Tour.objects.all()
        continent_id = self.request.query_params.get('continent', None)
        countery_id = self.request.query_params.get('countery', None)
        city_id = self.request.query_params.get('city', None)
        if countery_id:
            queryset.filter(tours__city__counteris__id=countery_id)

        if continent_id:
            queryset.filter(tours__city__counnteris__continents__id=continent_id)
        if countery_id:
            queryset.filter(tours__city__countery__id=countery_id)
        if city_id:
            queryset.filter(tour_city__id=city_id)
        return queryset
    
class TourDetailView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    
    
class NavbarAPIView(APIView):
    def get(self, request):
        # Correctly prefetch related countries and cities
        continents = Continent.objects.prefetch_related('countries__cities').all()
        continent_data = NavbarContinentSerializer(continents, many=True).data
        
        visas = Visa.objects.all()
        visa_data = VisaSerializer(visas, many=True).data
        
        navbar = []
        for continent in continent_data:
            continent_entry = {
                "id": continent['id'],
                "name": f"تور {continent['name']}",
                "path": f"/tour/?continent_id={continent['id']}",
                "children": []
            }
            for country in continent.get('countries', []):
                country_entry = {
                    "id": country['id'],
                    "name": country['name'],
                    "path": f"/tour/?country_id={country['id']}",
                    "children": []
                }
                for city in country.get('cities', []):
                    city_entry = {
                        "id": city['id'],
                        "name": city['name'],
                        "path": f"/tour/?city_id={city['id']}"
                    }
                    country_entry["children"].append(city_entry)

                continent_entry["children"].append(country_entry)

            navbar.append(continent_entry)
            
        visa_entry={
            "id": 3,
            "name": "ویزا",
            "children": []
        }
        for visa in visa_data:
            children = {
                "id": visa['id'],
                "name": f"ویزای {visa['title']}",
                "path": f"/visa/visas/?visa={visa['id']}"
            }
            visa_entry["children"].append(children)
        navbar.append(visa_entry)
            
        blog = {
            "id": 4,
            "name": "وبلاگ",
            "path": "/blog"
        }
        about = {
            "id": 5,
            "name": "درباره ما",
            "path": "/about-us"
        }
        contact = {
            "id": 6,
            "name": "تماس با ما",
            "path": "/contact-us"
        }
        navbar.append(blog)
        navbar.append(about)
        navbar.append(contact)
        return Response(navbar)