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
