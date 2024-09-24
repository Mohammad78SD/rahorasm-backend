from django.urls import path
from .views import ContactDetailList, AboutDetailList

urlpatterns = [
    path('contactus/', ContactDetailList.as_view(), name='contactus'),
    path('aboutus/', AboutDetailList.as_view(), name='aboutus'),
]