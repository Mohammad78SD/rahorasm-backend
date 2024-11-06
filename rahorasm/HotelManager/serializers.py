from rest_framework import serializers
from .models import HotelPrice, Hotel, HotelFacilities, RoomFacilities, RecreationalFacilities, SportFacilities

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
        


class HotelSerializer(serializers.ModelSerializer):
    hotel_facilities = HotelFacilitiesSerializer(many=True, read_only=True)
    room_facilities = RoomFacilitiesSerializer(many=True, read_only=True)
    recreational_facilities = RecreationalFacilitiesSerializer(many=True, read_only=True)
    sport_facilities = SportFacilitiesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'

class HotelPriceSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    class Meta:
        model = HotelPrice
        fields = '__all__'