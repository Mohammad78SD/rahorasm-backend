from django.contrib import admin
from .models import Hotel, HotelPrice, HotelFacilities, RoomFacilities, RecreationalFacilities, SportFacilities, HotelImage

#i want to add inline field to add images to hotel in admin panel
class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1
    fields = ('image','created_at')
    readonly_fields = ('created_at', 'edited_at')
    show_change_link = True
    verbose_name = "تصویر"
    verbose_name_plural = "تصاویر"

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline]

admin.site.register(Hotel, HotelAdmin)


admin.site.register(HotelPrice)
admin.site.register(HotelFacilities)
admin.site.register(RoomFacilities)
admin.site.register(RecreationalFacilities)
admin.site.register(SportFacilities)
admin.site.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'caption', 'uploaded_at')
    list_filter = ('hotel', 'uploaded_at')
    search_fields = ('caption', 'hotel__name')