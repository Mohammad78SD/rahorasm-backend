from rest_framework import serializers
from .models import City, Country, AirLine, Airport, Package, Tour

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class AirLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirLine
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    country = CountrySerializer()
    class Meta:
        model = Airport
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    country = CountrySerializer()
    class Meta:
        model = Package
        fields = '__all__'

class TourSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    airline = AirLineSerializer()
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    class Meta:
        model = Tour
        fields = '__all__'