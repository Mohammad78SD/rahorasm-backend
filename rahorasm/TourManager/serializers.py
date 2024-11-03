from rest_framework import serializers
from .models import City, Country, AirLine, Airport, Tour, Continent, Flight
import jdatetime
import pytz


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
    # arrival = serializers.SerializerMethodField()
    return_departure = serializers.SerializerMethodField()
    return_arrival = serializers.SerializerMethodField()
    
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    return_origin_airport = AirportSerializer()
    return_destination_airport = AirportSerializer()
    airline = AirLineSerializer()
    tour = TourInFlightSerializer()
    class Meta:
        model = Flight
        fields = '__all__'
        
    def get_departure(self, obj):
        jdate = obj.departure
        print(jdate.tzinfo)
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
    flights = FlightSerializer(many=True, read_only=True)
    class Meta:
        model = Tour
        fields = '__all__'





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