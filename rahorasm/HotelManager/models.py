from django.db import models
from django_jalali.db import models as jmodels
from TourManager.models import City, Flight
from django_ckeditor_5.fields import CKEditor5Field

        
class HotelFacilities(models.Model):
    name = models.CharField(max_length=200)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات هتل"
        
class RoomFacilities(models.Model):
    name = models.CharField(max_length=200)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات اتاق"
        
class RecreationalFacilities(models.Model):
    name = models.CharField(max_length=200)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات تفریحی"
        
class SportFacilities(models.Model):
    name = models.CharField(max_length=200)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات ورزشی"
        
class HotelImage(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='hotel_images')
    image = models.ImageField(upload_to='hotel_images/')
    alt = models.CharField(max_length=200, null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.hotel.name
    class Meta:
        verbose_name = "تصویر هتل"
        verbose_name_plural = "تصاویر هتل"
    
        
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    is_featured = models.BooleanField(default=False)
    star = models.IntegerField(choices=[(1, '1 ستاره'), (2, '2 ستاره'), (3, '3 ستاره'), (4, '4 ستاره'), (5, '5 ستاره'), (6, '6 ستاره')], default=1)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    location_on_map = models.CharField(max_length=200, null=True, blank=True)
    hotel_facilities = models.ManyToManyField(HotelFacilities, related_name='hotel_facilities')
    room_facilities = models.ManyToManyField(RoomFacilities, related_name='room_facilities')
    recreational_facilities = models.ManyToManyField(RecreationalFacilities, related_name='recreational_facilities')
    sport_facilities = models.ManyToManyField(SportFacilities, related_name='sport_facilities')
    description = models.TextField()
    long_description = CKEditor5Field('توضیح بیشتر', config_name='extends', null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "هتل"
        verbose_name_plural = "هتل ها"
        
class HotelPrice(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_prices')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flight_hotels')
    two_bed_price = models.DecimalField(max_digits=20, decimal_places=2)
    one_bed_price = models.DecimalField(max_digits=20, decimal_places=2)
    child_with_bed_price = models.DecimalField(max_digits=20, decimal_places=2)
    child_no_bed_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.hotel.name} - {self.flight.tour.title}'

    class Meta:
        verbose_name = "قیمت هتل"
        verbose_name_plural = "قیمت های هتل"