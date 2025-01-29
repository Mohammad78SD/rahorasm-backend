from django.contrib import admin
from .models import Hotel, HotelPrice, HotelFacilities, RoomFacilities, RecreationalFacilities, SportFacilities, HotelImage
from django import forms


# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1
    fields = ('image','created_at')
    readonly_fields = ('created_at', 'edited_at')
    show_change_link = True
    verbose_name = "تصویر"
    verbose_name_plural = "تصاویر"

class HotelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['city', 'hotel_facilities', 'room_facilities', 'recreational_facilities', 'sport_facilities']
    inlines = [HotelImageInline]

admin.site.register(Hotel, HotelAdmin)



class HotelPriceForm(forms.ModelForm):
    class Meta:
        model = HotelPrice
        fields = '__all__'  # Include all fields in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format the initial values of price fields if they exist
        for field in ['two_bed_price', 'one_bed_price', 'child_with_bed_price', 'child_no_bed_price']:
            if self.instance and getattr(self.instance, field) is not None:
                # Format the price for display
                self.fields[field].initial = "{:,.2f}".format(getattr(self.instance, field))



class HotelPriceAdmin(admin.ModelAdmin):
    form = HotelPriceForm
    autocomplete_fields = ['hotels']
    search_fields = ['hotels__name']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    # list_display = ('formatted_two_bed_price', 'formatted_one_bed_price', 
    #                 'formatted_child_with_bed_price', 'formatted_child_no_bed_price')

    # def formatted_two_bed_price(self, obj):
    #     return "${:,.2f}".format(obj.two_bed_price)
    # formatted_two_bed_price.short_description = "قیمت دو تخته"

    # def formatted_one_bed_price(self, obj):
    #     return "${:,.2f}".format(obj.one_bed_price)
    # formatted_one_bed_price.short_description = "قیمت یک تخته"

    # def formatted_child_with_bed_price(self, obj):
    #     return "${:,.2f}".format(obj.child_with_bed_price)
    # formatted_child_with_bed_price.short_description = "قیمت کودک با تخت"

    # def formatted_child_no_bed_price(self, obj):
    #     return "${:,.2f}".format(obj.child_no_bed_price)
    # formatted_child_no_bed_price.short_description = "قیمت کودک بدون تخت"

    # def save_model(self, request, obj, form, change):
    #     # Convert formatted string back to Decimal before saving
    #     for field in ['two_bed_price', 'one_bed_price', 'child_with_bed_price', 'child_no_bed_price']:
    #         price_str = form.cleaned_data[field].replace(',', '')  # Remove commas
    #         obj.__setattr__(field, price_str)  # Set the cleaned price value
    #     super().save_model(request, obj, form, change)

admin.site.register(HotelPrice, HotelPriceAdmin)





class HotelFacilitiesAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(HotelFacilities, HotelFacilitiesAdmin)
class RoomFacilitiesAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(RoomFacilities, RoomFacilitiesAdmin)
class RecreationalFacilitiesAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(RecreationalFacilities, RecreationalFacilitiesAdmin)
class SportFacilitiesAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(SportFacilities, SportFacilitiesAdmin)
class HotelImageAdmin(admin.ModelAdmin):
    search_fields = ('caption', 'hotel__name')
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
admin.site.register(HotelImage, HotelImageAdmin)