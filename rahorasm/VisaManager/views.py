from rest_framework import generics
from .models import Visa
from .serializers import VisaSerializer

class VisaListCreateView(generics.ListAPIView):
    queryset = Visa.objects.all()
    serializer_class = VisaSerializer

class VisaDetailView(generics.RetrieveAPIView):
    queryset = Visa.objects.all()
    serializer_class = VisaSerializer