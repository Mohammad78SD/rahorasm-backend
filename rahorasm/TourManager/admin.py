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


@admin.action(description="کپی کردن تور ها")
def duplicate_tour(modeladmin, request, queryset):
    for object in queryset:
        # Duplicate the object but set ID to None (so it creates a new instance)
        old_destinations = object.destinations.all()
        old_flight_times = object.flight_times.all()
        object.id = None
        object.pk = None  # Ensure the object is treated as new
        object.save()
        
        object.destinations.set(old_destinations)
        
        new_flight_times= []
        for flight_time in old_flight_times:
            old_flight_legs = flight_time.flight_Legs.all()
            old_hotel_prices = flight_time.hotel_price.all()
            flight_time.id = None
            flight_time.pk = None
            flight_time.save()
            new_flight_legs = []
            for flight_leg in old_flight_legs:
                flight_leg.id = None
                flight_leg.pk = None
                flight_leg.save()
                new_flight_legs.append(flight_leg)
            flight_time.flight_Legs.set(new_flight_legs)
            new_hotel_prices = []
            for hotel_price in old_hotel_prices:
                old_hotels = hotel_price.hotels.all()
                hotel_price.id = None
                hotel_price.pk = None
                hotel_price.save()
                hotel_price.hotels.set(old_hotels)
                new_hotel_prices.append(hotel_price)
            flight_time.hotel_price.set(new_hotel_prices)
            new_flight_times.append(flight_time)
                
        object.flight_times.set(new_flight_times)
        object.update_prices()
        object.save()
        
duplicate_tour.short_description = "کپی کردن تور ها"
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    autocomplete_fields = ['destinations']
    list_display = ('title', 'tour_type', 'is_featured', 'tour_duration')
    search_fields = ('title', 'description_editor')
    list_filter = ('tour_type', 'is_featured', 'is_shown')
    exclude = ('flight_times','least_price', 'max_price')
    inlines = [FlightTimesInline]
    actions = [duplicate_tour]
    
    
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
