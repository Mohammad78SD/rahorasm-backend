from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.db.models import OuterRef, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Country, AirLine, Airport, Tour, Continent
from VisaManager.models import Visa
from VisaManager.serializers import VisaSerializer
from .serializers import (
    CitySerializer,
    CountrySerializer,
    AirLineSerializer,
    AirportSerializer,
    TourSerializer,
    ContinentSerializer,
    NavbarContinentSerializer,
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

class CityListView(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CityFilter

class CountryListView(ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CountryFilter
class ContinentListView(ReadOnlyModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer
    filter_backends = (DjangoFilterBackend,)
class AirLineListView(ReadOnlyModelViewSet):
    queryset = AirLine.objects.all()
    serializer_class = AirLineSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AirLineFilter

class AirportListView(ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AirportFilter

    

class TourListView(ReadOnlyModelViewSet):
    serializer_class = TourSerializer
    queryset = Tour.objects.all()
    # @action(detail=False,methods=["get"]):
    # def getPackage()
    def list(self, request, *args, **kwargs):
        continentId= request.query_params.get('continent')
        counteryId = request.query_params.get('countery')
        cityId =  request.query_params.get('city')
        queryset=self.queryset
        if cityId :
            queryset.filter(city__id=cityId)
        elif counteryId:
            queryset.filter(city__countery__id=counteryId)
        elif continentId:
            queryset.filter(city__countery__continent__id=counteryId)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    
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
                "path": f"/tour/?continent={continent['id']}",
                "children": []
            }
            for country in continent.get('countries', []):
                country_entry = {
                    "id": country['id'],
                    "name": country['name'],
                    "path": f"/tour/country={country['id']}",
                    "children": []
                }
                for city in country.get('cities', []):
                    city_entry = {
                        "id": city['id'],
                        "name": city['name'],
                        "path": f"/tour/?city={city['id']}"
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