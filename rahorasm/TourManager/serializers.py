from rest_framework import serializers
from .models import City, Country, AirLine, Airport, Package, Tour, Continent


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

class TourSerializer(serializers.ModelSerializer):
    airline = AirLineSerializer()
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()

    class Meta:
        model = Tour
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    tours = TourSerializer(many=True, read_only=True)
    city = CitySerializer()

    class Meta:
        model = Package
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