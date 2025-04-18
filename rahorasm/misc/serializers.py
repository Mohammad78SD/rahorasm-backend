from rest_framework import serializers
from .models import ContactDetail, AboutDetail
from rest_framework import serializers
from .models import FooterBody, FooterColumn, FooterContact, MainPagePDF

class FooterBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterBody
        fields = ['title', 'link']

class FooterColumnSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()
    def get_body(self,obj):
        body = obj.body.all().order_by('sort')
        return FooterBodySerializer(body,many = True).data
    
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
        
class MainPagePDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPagePDF
        fields = '__all__'