from rest_framework import serializers
from .models import City, Country, AirLine, Airport, Tour, Continent, Flight
import jdatetime
import pytz
from HotelManager.serializers import HotelPriceSerializer

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

class FlightSerializer(serializers.ModelSerializer):
    departure = serializers.SerializerMethodField()
    return_departure = serializers.SerializerMethodField()
    return_arrival = serializers.SerializerMethodField()
    
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    return_origin_airport = AirportSerializer()
    return_destination_airport = AirportSerializer()
    airline = AirLineSerializer()
    tour = TourInFlightSerializer()
    
    hotel_prices = HotelPriceSerializer(many=True, read_only=True, source='flight_hotels')
    class Meta:
        model = Flight
        fields = '__all__'
        
    def get_departure(self, obj):
        jdate = obj.departure
        return jdate.togregorian()
    def get_arrival(self, obj):
        jdate = obj.arrival
        return jdate.togregorian()
    def get_return_departure(self, obj):
        jdate = obj.return_departure
        return jdate.togregorian()
    def get_return_arrival(self, obj):
        jdate = obj.return_arrival
        return jdate.togregorian()

class TourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    flights = FlightSerializer(many=True, read_only=True)
    start_date = serializers.SerializerMethodField()

    def get_start_date(self, obj):
        jdate = obj.start_date
        return jdate.togregorian()

    def get_image(self, obj):
        request = self.context.get('request')
        if request is None or not obj.image:
            return None
        return request.build_absolute_uri(obj.image.url)


    class Meta:
        model = Tour
        fields = '__all__'


class TourFlightsSerializer(serializers.ModelSerializer):
    departure = serializers.SerializerMethodField()
    return_departure = serializers.SerializerMethodField()
    def get_departure(self, obj):
        jdate = obj.departure
        return jdate.togregorian()
    def get_return_departure(self, obj):
        jdate = obj.return_departure
        return jdate.togregorian()
    class Meta:
        model = Flight
        fields = 'departure', 'return_departure', 'id'


class NavbarCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class NavbarCountrySerializer(serializers.ModelSerializer):
    cities = NavbarCitySerializer(many=True)  # Include cities

    class Meta:
        model = Country
        fields = '__all__'

class NavbarContinentSerializer(serializers.ModelSerializer):
    countries = NavbarCountrySerializer(many=True)  # Include countries

    class Meta:
        model = Continent
        fields = '__all__'