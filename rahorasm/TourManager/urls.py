from django.urls import path
from .views import (
    CityListView,
    CountryListView,
    AirLineListView,
    AirportListView,
    TourListView,
    NavbarAPIView,
    TourDetailView,
    FlightDetailView,
    Filters,
    TourFlights,
    Home,
    TourPDF
)

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city_list'),
    path('countries/', CountryListView.as_view(), name='country_list'),
    path('airlines/', AirLineListView.as_view(), name='airline_list'),
    path('airports/', AirportListView.as_view(), name='airport_list'),
    path('tours/', TourListView.as_view(), name='tour_list'),
    path('filters/', Filters.as_view(), name='tour_filters'),
    path('pdf/<int:pk>/', TourPDF, name='tour_pdf'),
    path('tour/<int:pk>/', TourDetailView.as_view(), name='tour_detail'),
    path('flight/<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),
    path('navbar/', NavbarAPIView.as_view(), name='navbar'),
    path('flights/<int:pk>/', TourFlights.as_view(), name='tour_flights'),
    path('home/', Home.as_view(), name='home'),
    

]