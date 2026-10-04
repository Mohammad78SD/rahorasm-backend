from rest_framework import serializers
from .models import Reserve, Person
from django.contrib.auth import get_user_model

User = get_user_model()


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "persian_name",
            "english_name",
            "national_code",
            "passport_number",
            "birth_date",
        ]


class ReserveSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)
    tour_name = serializers.CharField(source="tour.title", read_only=True)

    class Meta:
        model = Reserve
        fields = [
            "tour_name",
            "hotel_name",
            "two_bed_quantity",
            "one_bed_quantity",
            "child_with_bed_quantity",
            "child_no_bed_quantity",
            "final_price",
            "status",
        ]


class ReservePersonInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    en_name = serializers.CharField(max_length=100)
    ssn = serializers.CharField(max_length=10)
    passportNumber = serializers.CharField(max_length=10)
    birthday = serializers.CharField(max_length=10)


class ReserveCountInputSerializer(serializers.Serializer):
    # "identitication" (sic) is the field name the frontend already sends.
    identitication = serializers.ChoiceField(choices=[
        "two_bed_price", "one_bed_price", "child_with_bed_price", "child_no_bed_price",
    ])
    count = serializers.IntegerField(min_value=1)
    users = ReservePersonInputSerializer(many=True, required=False)


class CreateReserveSerializer(serializers.Serializer):
    flight_time_id = serializers.IntegerField()
    hotel_price_id = serializers.IntegerField()
    tour_id = serializers.IntegerField(required=False)
    count = ReserveCountInputSerializer(many=True, allow_empty=False)

    def validate(self, attrs):
        from HotelManager.models import HotelPrice
        from TourManager.models import FlightTimes, Tour
        try:
            flight_time = FlightTimes.objects.get(id=attrs["flight_time_id"])
        except FlightTimes.DoesNotExist:
            raise serializers.ValidationError({"flight_time_id": "Invalid flight time id"})
        try:
            hotel_price = HotelPrice.objects.get(id=attrs["hotel_price_id"])
        except HotelPrice.DoesNotExist:
            raise serializers.ValidationError({"hotel_price_id": "Invalid hotel price id"})
        if not flight_time.hotel_price.filter(id=hotel_price.id).exists():
            raise serializers.ValidationError(
                {"hotel_price_id": "This hotel price is not offered for the given flight time"})

        # A flight time can be attached to several tours (M2M). The client may say which
        # one with tour_id; without it the request is only valid if there is exactly one.
        tours = Tour.objects.filter(flight_times=flight_time)
        if "tour_id" in attrs:
            tours = tours.filter(id=attrs["tour_id"])
            if not tours.exists():
                raise serializers.ValidationError(
                    {"tour_id": "This tour does not use the given flight time"})
        elif tours.count() > 1:
            raise serializers.ValidationError(
                {"tour_id": "This flight time belongs to several tours; tour_id is required"})
        tour = tours.first()
        if tour is None:
            raise serializers.ValidationError({"flight_time_id": "This flight time does not belong to any tour"})

        attrs.update(flight_time=flight_time, hotel_price=hotel_price, tour=tour)
        return attrs
