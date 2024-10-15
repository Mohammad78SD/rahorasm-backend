from django.contrib import admin
from django.http import HttpRequest
from .models import City, Country, AirLine, Airport, Package, Tour, Continent,EuPackage,AsiaPackage
from durationwidget.widgets import TimeDurationWidget
from django import forms
from datetime import timedelta

class SplitDurationWidget(forms.MultiWidget):
    """
    A Widget that splits duration input into four number input boxes.
    """
    def __init__(self, attrs=None):
        widgets = (forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs))
        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = value
            if d:
                hours = d.seconds // 3600
                minutes = (d.seconds % 3600) // 60
                seconds = d.seconds % 60
                return [int(d.days), int(hours), int(minutes), int(seconds)]
        return [0, 1, 0, 0]
class MultiValueDurationField(forms.MultiValueField):
     widget = SplitDurationWidget

     def __init__(self, *args, **kwargs):
         fields = (
             forms.IntegerField(),
             forms.IntegerField(),
             forms.IntegerField(),
             forms.IntegerField(),
         )
         super(MultiValueDurationField, self).__init__(
             fields=fields,
             require_all_fields=True, *args, **kwargs)

     def compress(self, data_list):
         if len(data_list) == 4:
             return timedelta(
                 days=int(data_list[0]),
                 hours=int(data_list[1]),
                 minutes=int(data_list[2]),
                 seconds=int(data_list[3]))
         else:
             return timedelta(0)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(AirLine)
admin.site.register(Airport)
# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ["title","city__name",]

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    pass 
