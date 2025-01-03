import nested_admin
from django.contrib import admin
from .models import City, Country, AirLine, Airport, Tour, Continent, Flight
from HotelManager .models import HotelPrice
from django_jalali.admin.filters import JDateFieldListFilter

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(AirLine)
admin.site.register(Airport)


class HotelPriceInline(nested_admin.NestedStackedInline):
    model = HotelPrice
    extra = 0

class FlightInline(nested_admin.NestedStackedInline):
    model = Flight
    extra = 0
    inlines = [HotelPriceInline]    
    
    
@admin.register(Tour)
class TourAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'tour_type', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('tour_type', 'is_featured')
    ordering = ('-created_at',)
    inlines = [FlightInline]
    
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('tour', 'airline', 'departure', 'arrival', 'origin_airport', 'destination_airport', 'start_price')
    search_fields = ('tour__title', 'origin_airport__name', 'destination_airport__name')
    list_filter = ('tour', 'origin_airport', 'destination_airport')
    ordering = ('-departure',)
