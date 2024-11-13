from rest_framework import serializers
from .models import Reserve, Person
from django.contrib.auth import get_user_model
User = get_user_model()

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['persian_name', 'english_name', 'national_code', 'passport_number', 'birth_date']

class ReserveSerializer(serializers.ModelSerializer):
    persons = PersonSerializer(many=True, write_only=True)
    class Meta:
        model = Reserve
        fields = ['user', 'hotel', 'tour', 'flight', 'hotel_price', 'two_bed_quantity', 'one_bed_quantity', 
                  'child_with_bed_quantity', 'child_no_bed_quantity', 'final_price', 'status', 'persons']