from rest_framework import generics
from .models import ContactDetail, AboutDetail
from .serializers import ContactSerializer, AboutSerializer

class ContactDetailList(generics.ListAPIView):
    queryset = ContactDetail.objects.all()
    serializer_class = ContactSerializer
    
class AboutDetailList(generics.ListAPIView):
    queryset = AboutDetail.objects.all()
    serializer_class = AboutSerializer