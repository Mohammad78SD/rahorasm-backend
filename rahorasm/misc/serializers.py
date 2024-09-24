from rest_framework import serializers
from .models import ContactDetail, AboutDetail

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = '__all__'
        
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutDetail
        fields = '__all__'