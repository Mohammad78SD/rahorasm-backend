from django.contrib import admin
from .models import City, Country, AirLine, Airport, Tour, Continent, Flight

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(AirLine)
admin.site.register(Airport)

class FlightInline(admin.TabularInline):
    model = Flight
    extra = 1
    
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'tour_type', 'airline', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('tour_type', 'is_featured', 'airline')
    ordering = ('-created_at',)
    inlines = [FlightInline]

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('tour', 'departure', 'arrival', 'origin_airport', 'destination_airport', 'start_price')
    search_fields = ('tour__title', 'origin_airport__name', 'destination_airport__name')
    list_filter = ('tour', 'origin_airport', 'destination_airport')
    ordering = ('-departure',)
