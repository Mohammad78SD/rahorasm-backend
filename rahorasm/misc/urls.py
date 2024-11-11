from django.urls import path
from .views import ContactDetailList, AboutDetailList, footer_data

urlpatterns = [
    path('contactus/', ContactDetailList.as_view(), name='contactus'),
    path('aboutus/', AboutDetailList.as_view(), name='aboutus'),
    path('footer/', footer_data, name='footer'),
]