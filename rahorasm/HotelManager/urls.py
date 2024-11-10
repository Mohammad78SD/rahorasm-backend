from django.urls import path
from .views import HotelDetails, HotelList

urlpatterns = [
    path('<int:pk>/', HotelDetails.as_view(), name='hotel_details'),
    path('', HotelList.as_view(), name='hotel_list'),
]