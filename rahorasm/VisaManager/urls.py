from django.urls import path
from .views import VisaListCreateView, VisaDetailView

urlpatterns = [
    path('list/', VisaListCreateView.as_view(), name='visa-list-create'),
    path('<int:pk>/', VisaDetailView.as_view(), name='visa-detail'),
]