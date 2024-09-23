from django.contrib import admin
from .models import City, Country, AirLine, Airport, Package, Tour, Continent

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(AirLine)
admin.site.register(Airport)
admin.site.register(Package)
admin.site.register(Tour)
# Register your models here.
