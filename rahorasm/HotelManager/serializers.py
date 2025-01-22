from rest_framework import serializers
from .models import HotelPrice, Hotel, HotelFacilities, RoomFacilities, RecreationalFacilities, SportFacilities, HotelImage
from TourManager.models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']

class HotelFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelFacilities
        fields = ['name']

class RoomFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomFacilities
        fields = ['name']
    
class RecreationalFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecreationalFacilities
        fields = ['name']

class SportFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportFacilities
        fields = ['name']
        
import environ
env = environ.Env()
environ.Env.read_env()

class HotelImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HotelImage
        fields = ['id', 'image', 'alt']

    def get_image(self, obj):
        if obj.image:
            return f"{env('BACKEND_URL')}{settings.MEDIA_URL}{obj.image}"  # Construct the URL using MEDIA_URL
        return None


class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True, read_only=True, source='hotel_images')
    
    hotel_facilities = HotelFacilitiesSerializer(many=True, read_only=True)
    room_facilities = RoomFacilitiesSerializer(many=True, read_only=True)
    recreational_facilities = RecreationalFacilitiesSerializer(many=True, read_only=True)
    sport_facilities = SportFacilitiesSerializer(many=True, read_only=True)
    
    city = CitySerializer()
    
    class Meta:
        model = Hotel
        fields = '__all__'

class HotelPriceSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True, read_only=True)
    class Meta:
        model = HotelPrice
        fields = '__all__'