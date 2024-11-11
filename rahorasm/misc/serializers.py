from rest_framework import serializers
from .models import ContactDetail, AboutDetail
from rest_framework import serializers
from .models import FooterBody, FooterColumn, FooterContact

class FooterBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterBody
        fields = ['title', 'link']

class FooterColumnSerializer(serializers.ModelSerializer):
    body = FooterBodySerializer(many=True, read_only=True)
    
    class Meta:
        model = FooterColumn
        fields = ['title', 'body']

class FooterContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterContact
        fields = ['title', 'address', 'work_time', 'phone', 
                 'email', 'instagram', 'telegram', 'whatsapp']
        

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = '__all__'
        
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutDetail
        fields = '__all__'