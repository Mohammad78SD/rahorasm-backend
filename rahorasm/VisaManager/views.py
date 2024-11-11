from rest_framework import generics
from .models import Visa
from .serializers import VisaSerializer, VisaListSerializer

class VisaListCreateView(generics.ListAPIView):
    queryset = Visa.objects.all()
    serializer_class = VisaSerializer

class VisaDetailView(generics.RetrieveAPIView):
    queryset = Visa.objects.all()
    serializer_class = VisaSerializer
    
class VisaListView(generics.ListAPIView):
    queryset = Visa.objects.all()
    serializer_class = VisaListSerializer