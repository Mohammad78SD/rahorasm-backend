from django.urls import path
from .views import VisaListCreateView, VisaDetailView

urlpatterns = [
    path('visas/', VisaListCreateView.as_view(), name='visa-list-create'),
    path('visas/<int:pk>/', VisaDetailView.as_view(), name='visa-detail'),
]