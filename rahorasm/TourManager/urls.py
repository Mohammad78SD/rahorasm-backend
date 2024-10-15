from django.urls import path
from .views import (
    CityListView,
    CountryListView,
    ContinentListView,
    AirLineListView,
    AirportListView,
    NavbarAPIView,
    TourListView,
)
from rest_framework import routers
router = routers.SimpleRouter()
router.register('city',CityListView)
router.register('countery',CountryListView)
router.register('continet',ContinentListView)
router.register('airlines',AirLineListView)
router.register('airports',AirportListView)
router.register('tours/',TourListView)

urlpatterns = [
    path('navbar/', NavbarAPIView.as_view(), name='navbar'),
]+router.urls