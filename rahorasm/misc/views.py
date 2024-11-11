from rest_framework import generics
from .models import ContactDetail, AboutDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import FooterBody, FooterColumn, FooterContact
from .serializers import (FooterBodySerializer, FooterColumnSerializer, 
                        FooterContactSerializer, ContactSerializer, AboutSerializer)

class ContactDetailList(generics.ListAPIView):
    queryset = ContactDetail.objects.all()
    serializer_class = ContactSerializer
    
class AboutDetailList(generics.ListAPIView):
    queryset = AboutDetail.objects.all()
    serializer_class = AboutSerializer

@api_view(['GET'])
def footer_data(request):
    
    columns = FooterColumn.objects.all()
    contact = FooterContact.objects.first()
    
    data = {
        'columns': FooterColumnSerializer(columns, many=True).data,
        'contact': FooterContactSerializer(contact).data if contact else None
    }
    
    return Response(data)
