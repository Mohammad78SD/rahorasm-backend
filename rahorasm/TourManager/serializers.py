from rest_framework import serializers
from .models import City, Country, AirLine, Airport, Tour, Continent, FlightLeg, FlightTimes
import jdatetime
import pytz
from HotelManager.serializers import HotelPriceSerializer
from django.conf import settings

class AirLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirLine
        fields = '__all__'

class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    continent = ContinentSerializer()

    class Meta:
        model = Country
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = City
        fields = '__all__'
class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)
class AirportSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Airport
        fields = '__all__'

class TourInFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'


class FlightLegSerializer(serializers.ModelSerializer):
    airline = AirLineSerializer()
    departure_airport = AirportSerializer()
    arrival_airport = AirportSerializer()
    departure = serializers.SerializerMethodField()
    arrival = serializers.SerializerMethodField()

    # destination_airport = AirportSerializer()
    # return_origin_airport = AirportSerializer()
    # return_destination_airport = AirportSerializer()
    # tour = TourInFlightSerializer()
    
    # hotel_prices = HotelPriceSerializer(many=True, read_only=True, source='flight_hotels')
    class Meta:
        model = FlightLeg
        fields = '__all__'
        
    def get_departure(self, obj):
        jdate = obj.departure_time
        return jdate.togregorian()
    def get_arrival(self, obj):
        jdate = obj.arrival_time
        return jdate.togregorian()

class FlightSerializer(serializers.ModelSerializer):
    departure_date = serializers.SerializerMethodField()
    arrival_date = serializers.SerializerMethodField()
    flight_Legs = FlightLegSerializer(many=True, read_only=True)
    hotel_price = HotelPriceSerializer(many=True, read_only=True, source='flight_hotels')
    tour = serializers.SerializerMethodField()
    
    class Meta:
        model = FlightTimes
        fields = '__all__'
        
    def get_departure_date(self, obj):
        jdate = obj.departure_date
        return jdate.togregorian()
    def get_arrival_date(self, obj):
        jdate = obj.arrival_date
        return jdate.togregorian()
    def get_tour(self, obj):
        serializers = TourSerializer(Tour.objects.get(flight_times=obj))
        return serializers.data

class FlightTimeSerializer(serializers.ModelSerializer):
    
    departure_date = serializers.SerializerMethodField()
    arrival_date = serializers.SerializerMethodField()
    flight_Legs = FlightLegSerializer(many=True, read_only=True)
    hotel_price = serializers.SerializerMethodField()

    def get_hotel_price(self, obj):
        hotel_prices = obj.hotel_price.all().order_by('two_bed_price')
        return HotelPriceSerializer(hotel_prices, many=True).data
    least_price = serializers.SerializerMethodField()
    least_price_currency = serializers.SerializerMethodField()
    other_currency = serializers.SerializerMethodField()
    
    
    def get_least_price(self, obj):
        return self.get_least_prices(obj)['least_price']
    
    def get_least_price_currency(self, obj):
        return self.get_least_prices(obj)['least_price_other_currency']
    
    def get_currency(self, obj):
        return self.get_least_prices(obj)['currency']
    
    def get_least_prices(self, obj):
        prices = obj.hotel_price.all()  # Corrected the related name
        least_price = None  # Start with None to handle no prices
        least_price_other_currency = None
        currency = None
        
        for price in prices:
            # Compare using the Decimal type
            if least_price is None or price.two_bed_price < least_price:
                least_price = price.two_bed_price
                least_price_other_currency = price.two_bed_price_other_currency
                currency = price.other_currency

        return {
            'least_price': least_price,
            'least_price_other_currency': least_price_other_currency,
            'currency': currency
        }  # Returns None if no prices are found
    
    def get_departure_date(self, obj):
        jdate = obj.departure_date
        return jdate.togregorian()
    def get_arrival_date(self, obj):
        jdate = obj.arrival_date
        return jdate.togregorian()

    class Meta:
        model = FlightTimes
        fields = '__all__'
        
import environ
env = environ.Env()
environ.Env.read_env()
    
class TourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    destinations = CitySerializer(many=True)
    flight_times = FlightTimeSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Tour
        fields = '__all__'
        
    def get_start_date(self, obj):
        jdate = obj.start_date
        return jdate.togregorian()

    def get_image(self, obj):
        if obj.image:
            return f"{env('BACKEND_URL')}{settings.MEDIA_URL}{obj.image}"  # Construct the URL using MEDIA_URL
        return None




class TourFlightsSerializer(serializers.ModelSerializer):
    departure = serializers.SerializerMethodField()
    return_departure = serializers.SerializerMethodField()
    flight_Legs = FlightLegSerializer(many=True, read_only=True)
    hotel_price = HotelPriceSerializer(many=True, read_only=True)   
    def get_departure(self, obj):
        jdate = obj.departure_date
        return jdate.togregorian()
    def get_return_departure(self, obj):
        jdate = obj.arrival_date
        return jdate.togregorian()
    class Meta:
        model = FlightTimes
        fields = '__all__'


class NavbarCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class NavbarCountrySerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()
    def get_cities(self, obj):
        cities = obj.cities.all().order_by('sort')
        return NavbarCitySerializer(cities, many=True).data
    class Meta:
        model = Country
        fields = '__all__'

class NavbarContinentSerializer(serializers.ModelSerializer):
    countries = serializers.SerializerMethodField()
    def get_countries(self, obj):
        countries = obj.countries.all().order_by('sort')
        return NavbarCountrySerializer(countries, many=True).data
    class Meta:
        model = Continent
        fields = '__all__'