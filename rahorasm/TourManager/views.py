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
    NavbarCountrySerializer,
    TourFlightsSerializer,
    CityListSerializer,
)
from .filters import (
    CityFilter,
    CountryFilter,
    AirLineFilter,
    AirportFilter,
    TourFilter,
)
from rest_framework.filters import OrderingFilter
from HotelManager.models import Hotel
from HotelManager.serializers import HotelSerializer
from blog.models import Category

class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
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
            
            
        duration = self.request.query_params.get('duration', None)
        if duration:
            duration_list = [d.strip() for d in duration.split(',')]
            queryset = queryset.filter(tour_duration__in=duration_list)
        
        
        airline_ids = self.request.query_params.get('airline', None)
        if airline_ids:
            # Split the airline string by commas and filter
            airline_list = [airline_id.strip() for airline_id in airline_ids.split(',')]
            queryset = queryset.filter(flights__airline__id__in=airline_list).distinct()
            
            
            
        max_price = self.request.query_params.get('max_price', None)
        least_price = self.request.query_params.get('least_price', None)
        if max_price:
            queryset = queryset.filter(least_price__lte=max_price)
        if least_price:
            queryset = queryset.filter(least_price__gte=least_price)
        
        

        ordering = self.request.query_params.get('order_by', None)
        
        if ordering == 'max_price':
            queryset = queryset.order_by('-least_price')
        elif ordering == 'least_price':
            queryset = queryset.order_by(ordering)
        elif ordering == 'max_duration':
            queryset = queryset.order_by('-tour_duration')
        elif ordering == 'least_duration':
            queryset = queryset.order_by('tour_duration')
        
        #i want to filter tours if the is_shown is true or not
        queryset = queryset.filter(is_shown=True)
        return queryset
    
def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    airline_ids = request.query_params.get('airline', None)
    max_price = request.query_params.get('max_price', None)
    least_price = request.query_params.get('least_price', None)
    
    response_data = []
    
    for tour in queryset:
        # Start with all flights for this tour
        flights = tour.flights.all()
        
        # Filter flights by airline_ids if provided
        if airline_ids:
            airline_list = [airline_id.strip() for airline_id in airline_ids.split(',')]
            flights = flights.filter(airline__id__in=airline_list)
        
        # Filter flights by max_price if provided
        if max_price:
            flights = flights.filter(start_price__lte=max_price)
        
        # Filter flights by least_price if provided
        if least_price:
            flights = flights.filter(start_price__gte=least_price)
        
        # Serialize filtered flights
        flights_data = FlightSerializer(flights, many=True).data
        
        # Serialize the tour and include the filtered flights
        tour_data = TourSerializer(tour).data
        tour_data['flights'] = flights_data
        response_data.append(tour_data)
    
    return Response(response_data)

    
class TourDetailView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    
class FlightDetailView(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    
    
class TourFlights(APIView):
    def get(self, request, pk):
        flights = Flight.objects.all().filter(tour__id=pk)
        serializer = TourFlightsSerializer(flights, many=True)
        return Response(serializer.data)
    
    
    
class Filters(APIView):
    def get(self, request):
        city_name = self.request.query_params.get('city', None)
        country_name = self.request.query_params.get('country', None)
        continent_name = self.request.query_params.get('continent', None)

        airlinefilter = []
        duration_filter = []
        price_filter = {
            "least_price": 0,
            "max_price": 0
        }
        if city_name:
            airlines = AirLine.objects.all().filter(flight_airlines__tour__destination__name=city_name).distinct()
            for airline in airlines:
                flights_quantity = Flight.objects.all().filter(airline=airline, tour__destination__name=city_name).count()
                airlinefilter.append({
                    "id": airline.id,
                    "name": airline.name,
                    "tours_quantity": flights_quantity
                })
            
            durations = Tour.objects.all().filter(destination__name=city_name).values('tour_duration').distinct()
            for duration in durations:
                tours_quantity = Tour.objects.all().filter(destination__name=city_name, tour_duration=duration['tour_duration']).count()
                duration_filter.append({
                    "duration": duration['tour_duration'],
                    "tours_quantity": tours_quantity
                })
            
            max_price = Tour.objects.all().filter(destination__name=city_name).order_by('-max_price').first()
            least_price = Tour.objects.all().filter(destination__name=city_name).order_by('least_price').first()
            if(max_price):
                price_filter['max_price'] = max_price.max_price
            if(least_price):
                price_filter['least_price'] = least_price.least_price
                
        if country_name:
            airlines = AirLine.objects.all().filter(flight_airlines__tour__destination__country__name=country_name).distinct()
            for airline in airlines:
                flights_quantity = Flight.objects.all().filter(airline=airline, tour__destination__country__name=country_name).count()
                airlinefilter.append({
                    "id": airline.id,
                    "name": airline.name,
                    "tours_quantity": flights_quantity
                })
                
            durations = Tour.objects.all().filter(destination__country__name=country_name).values('tour_duration').distinct()
            for duration in durations:
                tours_quantity = Tour.objects.all().filter(destination__country__name=country_name, tour_duration=duration['tour_duration']).count()
                duration_filter.append({
                    "duration": duration['tour_duration'],
                    "tours_quantity": tours_quantity
                })
            max_price = Tour.objects.all().filter(destination__country__name=country_name).order_by('-max_price').first()
            least_price = Tour.objects.all().filter(destination__country__name=country_name).order_by('least_price').first()
            price_filter['max_price'] = max_price.max_price
            price_filter['least_price'] = least_price.least_price
                
                
        if continent_name:
            airlines = AirLine.objects.all().filter(flight_airlines__tour__destination__country__continent__name=continent_name).distinct()
            for airline in airlines:
                flights_quantity = Flight.objects.all().filter(airline=airline, tour__destination__country__continent__name=continent_name).count()
                airlinefilter.append({
                    "id": airline.id,
                    "name": airline.name,
                    "tours_quantity": flights_quantity
                })
                
            durations = Tour.objects.all().filter(destination__country__continent__name=continent_name).values('tour_duration').distinct()
            for duration in durations:
                tours_quantity = Tour.objects.all().filter(destination__country__continent__name=continent_name, tour_duration=duration['tour_duration']).count()
                duration_filter.append({
                    "duration": duration['tour_duration'],
                    "tours_quantity": tours_quantity
                })
            max_price = Tour.objects.all().filter(destination__country__continent__name=continent_name).order_by('-max_price').first()
            least_price = Tour.objects.all().filter(destination__country__continent__name=continent_name).order_by('least_price').first()
            price_filter['max_price'] = max_price.max_price
            price_filter['least_price'] = least_price.least_price    
        
        return Response({
            "airlines": airlinefilter,
            "durations": duration_filter,
            "prices": price_filter
        })
        
        
        
class NavbarAPIView(APIView):
    def get(self, request):
        # Correctly prefetch related countries and cities
        continents = Continent.objects.prefetch_related('countries__cities').all()
        continent_data = NavbarContinentSerializer(continents, many=True).data
        blog_categories = Category.objects.all()

        visas = Visa.objects.all()
        visa_data = VisaSerializer(visas, many=True).data
        
        
        
        navbar = []
        for continent in continent_data:
            continent_entry = {
                "id": continent['id'],
                "name": f"تور {continent['name']}",
                "path": f"/tour/tours?continent={continent['name']}",
                "children": []
            }
            for country in continent.get('countries', []):
                country_entry = {
                    "id": country['id'],
                    "name": country['name'],
                    "path": f"/tour/tours?country={country['name']}",
                    "children": []
                }
                for city in country.get('cities', []):
                    city_entry = {
                        "id": city['id'],
                        "name": city['name'],
                        "path": f"/tour/tours?city={city['name']}"
                    }
                    country_entry["children"].append(city_entry)

                continent_entry["children"].append(country_entry)

            navbar.append(continent_entry)
            
        visa_entry={
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
        
        
        hotels = {
            "name": "هتل ها",
            "children": []
        }
        for continent in continent_data:
            hotels_continent_entry = {
                "id": continent['id'],
                "name": f"هتل های {continent['name']}یی",
                "path": f"hotel?continent={continent['name']}",
                "children": []
            }
            for country in continent.get('countries', []):
                hotels_country_entry = {
                    "id": country['id'],
                    "name": f"هتل های {country['name']}",
                    "path": f"/hotel?country={country['name']}",
                }
                hotels_continent_entry["children"].append(hotels_country_entry)
            hotels["children"].append(hotels_continent_entry)
        navbar.append(hotels)
        
        blog = {
            "name": "وبلاگ",
            "path": "/blog",
            "children": []
        }
        for category in blog_categories:
            blog_category = {
                "id": category.id,
                "name": category.title,
                "path": f"/blog?category={category.id}"
            }
            blog["children"].append(blog_category)
        
        about = {
            "name": "درباره ما",
            "path": "/about"
        }
        contact = {
            "name": "تماس با ما",
            "path": "/contact"
        }
        navbar.append(blog)
        navbar.append(about)
        navbar.append(contact)
        return Response(navbar)
    
    
class Home(APIView):
    def get(self, request):
        featured_tours = Tour.objects.all().filter(is_featured=True).order_by('-created_at')[:10]
        featured_tours_serializer = TourSerializer(featured_tours, many=True, context={'request': request})
        
        latest_asia_tours = Tour.objects.all().filter(destination__country__continent__name='آسیا').order_by('-created_at')[:10]
        latest_tours_serializer = TourSerializer(latest_asia_tours, many=True, context={'request': request})
        
        latest_europe_tours = Tour.objects.all().filter(destination__country__continent__name='اروپا').order_by('-created_at')[:10]
        latest_europe_tours_serializer = TourSerializer(latest_europe_tours, many=True, context={'request': request})
        
        featured_hotels = Hotel.objects.all().filter(is_featured=True).order_by('-created_at')[:10]
        featured_hotels_serializer = HotelSerializer(featured_hotels, many=True, context={'request': request})
        
        return Response({
            "featured_tours": featured_tours_serializer.data,
            "latest_asia_tours": latest_tours_serializer.data,
            "latest_europe_tours": latest_europe_tours_serializer.data,
            "featured_hotels": featured_hotels_serializer.data
        })