from django.urls import path
from .views import (
    CityListView,
    CountryListView,
    AirLineListView,
    AirportListView,
    PackageListView,
    TourListView,
    NavbarAPIView,
    TourDetailView,
)

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city_list'),
    path('countries/', CountryListView.as_view(), name='country_list'),
    path('airlines/', AirLineListView.as_view(), name='airline_list'),
    path('airports/', AirportListView.as_view(), name='airport_list'),
    path('packages/', PackageListView.as_view(), name='package_list'),
    path('tours/', TourListView.as_view(), name='tour_list'),
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour_detail'),
    path('navbar/', NavbarAPIView.as_view(), name='navbar'),

]