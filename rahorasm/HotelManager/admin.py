from django.contrib import admin
from .models import Hotel, HotelPrice, HotelFacilities, RoomFacilities, RecreationalFacilities, SportFacilities

# Register your models here.
admin.site.register(Hotel)
admin.site.register(HotelPrice)
admin.site.register(HotelFacilities)
admin.site.register(RoomFacilities)
admin.site.register(RecreationalFacilities)
admin.site.register(SportFacilities)