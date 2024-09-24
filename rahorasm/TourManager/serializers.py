from rest_framework import serializers
from .models import City, Country, AirLine, Airport, Package, Tour, Continent

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AirLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirLine
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    country = CountrySerializer()

    class Meta:
        model = Airport
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    airline = AirLineSerializer()
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    path = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = '__all__'

    def get_path(self, obj):
        return f"/{obj.package.country.name}-tour-{obj.title}"


class PackageSerializer(serializers.ModelSerializer):
    tours = TourSerializer(many=True, read_only=True)
    city = CitySerializer()
    country = CountrySerializer()

    class Meta:
        model = Package
        fields = '__all__'


class ContinentSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Continent
        fields = ['id', 'name', 'countries']