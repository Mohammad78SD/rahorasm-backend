from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import jdatetime
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Country, AirLine, Airport, Tour, Continent, Flight
from VisaManager.models import Visa
from VisaManager.serializers import VisaSerializer
from .serializers import (
    CitySerializer,
    CountrySerializer,
    AirLineSerializer,
    AirportSerializer,
    TourSerializer,
    FlightSerializer,
    NavbarContinentSerializer,
    NavbarCountrySerializer
)
from .filters import (
    CityFilter,
    CountryFilter,
    AirLineFilter,
    AirportFilter,
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


class TourListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'destination__name': ['exact'],
        'destination__country__name': ['exact'],
        'destination__country__continent__name': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        city_name = self.request.query_params.get('city', None)
        country_name = self.request.query_params.get('country', None)
        continent_name = self.request.query_params.get('continent', None)
        
        is_featured = self.request.query_params.get('is_featured', None)

        if city_name:
            queryset = queryset.filter(destination__name=city_name)
        if country_name:
            queryset = queryset.filter(destination__country__name=country_name)
        if continent_name:
            queryset = queryset.filter(destination__country__continent__name=continent_name)
            
        if is_featured:
            queryset = queryset.filter(is_featured=True)

        ordering = self.request.query_params.get('order_by', None)
        print(ordering)
        if ordering:
            queryset = queryset.order_by(ordering)
            
        return queryset
    
class TourDetailView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    
class FlightDetailView(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    
    
    
class Filters(APIView):
    def get(self, request):
        city_name = self.request.query_params.get('city', None)
        country_name = self.request.query_params.get('country', None)
        continent_name = self.request.query_params.get('continent', None)
        airlinefilter = []
        if city_name:
            airlines = AirLine.objects.all().filter(flight_airlines__tour__destination__name=city_name).distinct()
            for airline in airlines:
                flights_quantity = Flight.objects.all().filter(airline=airline, tour__destination__name=city_name).count()
                airlinefilter.append({
                    "id": airline.id,
                    "name": airline.name,
                    "tours_quantity": flights_quantity
                })
        if country_name:
            airlines = AirLine.objects.all().filter(flight_airlines__tour__destination__country__name=country_name).distinct()
            for airline in airlines:
                flights_quantity = Flight.objects.all().filter(airline=airline, tour__destination__country__name=country_name).count()
                airlinefilter.append({
                    "id": airline.id,
                    "name": airline.name,
                    "tours_quantity": flights_quantity
                })
        if continent_name:
            airlines = AirLine.objects.all().filter(flight_airlines__tour__destination__country__continent__name=continent_name).distinct()
            for airline in airlines:
                flights_quantity = Flight.objects.all().filter(airline=airline, tour__destination__country__continent__name=continent_name).count()
                airlinefilter.append({
                    "id": airline.id,
                    "name": airline.name,
                    "tours_quantity": flights_quantity
                })

        
        return Response({
            "airlines": airlinefilter,
        })
        
        
        
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
                "path": f"/tour/tours/?continent{continent['name']}",
                "children": []
            }
            for country in continent.get('countries', []):
                country_entry = {
                    "id": country['id'],
                    "name": country['name'],
                    "path": f"/tour/tours/?country{country['name']}",
                    "children": []
                }
                for city in country.get('cities', []):
                    city_entry = {
                        "id": city['id'],
                        "name": city['name'],
                        "path": f"/tour/tours/?city{city['name']}"
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
                "path": f"/visa/{visa['id']}"
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
            "path": "/about"
        }
        contact = {
            "id": 6,
            "name": "تماس با ما",
            "path": "/contact"
        }
        navbar.append(blog)
        navbar.append(about)
        navbar.append(contact)
        return Response(navbar)