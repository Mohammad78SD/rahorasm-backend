from django.urls import path
from .views import VisaListCreateView, VisaDetailView, VisaListView

urlpatterns = [
    path('list/', VisaListCreateView.as_view(), name='visa-list-create'),
    path('search/', VisaListView.as_view(), name='visa-list-search'),
    path('<int:pk>/', VisaDetailView.as_view(), name='visa-detail'),
]