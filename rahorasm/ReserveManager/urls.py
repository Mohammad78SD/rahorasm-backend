from django.urls import path
from .views import CreateReserveView, ListReserveView, RetrieveReserveView

urlpatterns = [
    path('new/', CreateReserveView.as_view(), name='create-reserve'),
    path('list/', ListReserveView.as_view(), name='list-reserve'),
    path('<int:pk>/', RetrieveReserveView.as_view(), name='retrieve-reserve'),
]
