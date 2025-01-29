import nested_admin
from django.contrib import admin
from .models import City, Country, AirLine, Airport, Tour, Continent, FlightLeg, FlightTimes
from HotelManager .models import HotelPrice
from django_jalali.admin.filters import JDateFieldListFilter

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['country']
admin.site.register(City, CityAdmin)

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['continent']
admin.site.register(Country, CountryAdmin)

class ContinentAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Continent, ContinentAdmin)

class AirLineAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
admin.site.register(AirLine, AirLineAdmin)

class AirportAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['city']
admin.site.register(Airport, AirportAdmin)

class HotelPriceInline(admin.TabularInline):
    model = FlightTimes.hotel_price.through
    extra = 1
    autocomplete_fields = ['hotelprice']
    verbose_name = "قیمت هتل"
    verbose_name_plural = "قیمت هتل ها"
class FlightLegsInline(admin.TabularInline):
    model = FlightTimes.flight_Legs.through
    extra = 1
    autocomplete_fields = ['flightleg']
    verbose_name = "پرواز"
    verbose_name_plural = "پرواز ها"
class FlightTimesAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    search_fields = ['departure_time']
    inlines = [FlightLegsInline, HotelPriceInline]
    exclude = ('hotel_price', 'flight_Legs')
admin.site.register(FlightTimes, FlightTimesAdmin)


class FlightTimesInline(admin.TabularInline):  # or use StackedInline if you prefer a vertical layout
    model = Tour.flight_times.through  # Use the through model for the Many-to-Many relationship
    extra = 1  # Number of empty forms to show for adding new relations
    verbose_name = "تاریخ پرواز"  # Custom name for the inline
    verbose_name_plural = "تاریخ های پرواز"
    save_as = True
    
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    autocomplete_fields = ['destinations']
    list_display = ('title', 'tour_type', 'is_featured', 'tour_duration')
    search_fields = ('title', 'description_editor')
    list_filter = ('tour_type', 'is_featured', 'is_shown')
    exclude = ('flight_times',)
    inlines = [FlightTimesInline]
    
    
@admin.register(FlightLeg)
class FlightLegAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    autocomplete_fields = ['airline', 'departure_airport', 'arrival_airport']
    list_display = ('airline', 'departure_airport', 'arrival_airport')
    search_fields = ('departure_airport__name', 'arrival_airport__name')
    list_filter = ('departure_airport', 'arrival_airport')
    ordering = ('-departure_time',)
