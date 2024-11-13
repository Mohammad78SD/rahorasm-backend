from django.urls import path
from .views import CreateReserveView

urlpatterns = [
    path('new/', CreateReserveView.as_view(), name='create-reserve'),
]
