from django.db import models
from django_jalali.db import models as jmodels
from TourManager.models import City
from django_ckeditor_5.fields import CKEditor5Field

        
class HotelFacilities(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات هتل"
        verbose_name_plural = "امکانات هتل"
        
class RoomFacilities(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات اتاق"
        verbose_name_plural = "امکانات اتاق"
        
class RecreationalFacilities(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات تفریحی"
        verbose_name_plural = "امکانات تفریحی"
        
class SportFacilities(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "امکانات ورزشی"
        verbose_name_plural = "امکانات ورزشی"
        
class HotelImage(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='hotel_images', verbose_name="هتل")
    image = models.ImageField(upload_to='hotel_images/', verbose_name="تصویر")
    alt = models.CharField(max_length=200, null=True, blank=True, verbose_name="توضیح")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    def __str__(self):
        return self.hotel.name
    class Meta:
        verbose_name = "تصویر هتل"
        verbose_name_plural = "تصاویر هتل"
    
        
class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    english_name = models.CharField(max_length=200, verbose_name="نام انگلیسی", null=True, blank=True)
    address = models.TextField(verbose_name="آدرس")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    star = models.IntegerField(choices=[(1, '1 ستاره'), (2, '2 ستاره'), (3, '3 ستاره'), (4, '4 ستاره'), (5, '5 ستاره'), (6, '5 ستاره تاپ'), (0, 'هتل آپارتمان')], default=1, verbose_name="ستاره")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="شهر")
    location_on_map = models.CharField(max_length=200, null=True, blank=True, verbose_name="موقعیت روی نقشه")
    hotel_facilities = models.ManyToManyField(HotelFacilities, related_name='hotel_facilities', verbose_name="امکانات هتل")
    room_facilities = models.ManyToManyField(RoomFacilities, related_name='room_facilities', verbose_name="امکانات اتاق")
    recreational_facilities = models.ManyToManyField(RecreationalFacilities, related_name='recreational_facilities', verbose_name="امکانات تفریحی")
    sport_facilities = models.ManyToManyField(SportFacilities, related_name='sport_facilities', verbose_name="امکانات ورزشی")
    description = models.TextField(verbose_name="توضیحات")
    long_description = CKEditor5Field('توضیح بیشتر', config_name='extends', null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "هتل"
        verbose_name_plural = "هتل ها"
        
class HotelPrice(models.Model):
    hotels = models.ManyToManyField(Hotel, related_name='hotel_prices', verbose_name="هتل")
    two_bed_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="قیمت دو تخته")
    one_bed_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="قیمت یک تخته")
    child_with_bed_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="قیمت کودک با تخت")
    child_no_bed_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="قیمت کودک بدون تخت")
    other_currency = models.CharField(choices=[('EUR', 'یورو'), ('USD', 'دلار')], max_length=10, null=True, blank=True, verbose_name="ارز دیگر")
    two_bed_price_other_currency = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="قیمت دو تخته در ارز دیگر")
    one_bed_price_other_currency = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="قیمت یک تخته در ارز دیگر")
    child_with_bed_price_other_currency = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="قیمت کودک با تخت در ارز دیگر")
    child_no_bed_price_other_currency = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="قیمت کودک بدون تخت در ارز دیگر")
    
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def __str__(self):
        return ", ".join([i.name for i in self.hotels.all()]) + " با قیمت 2 تخته " + str(self.two_bed_price) + " تومان"

    class Meta:
        verbose_name = "قیمت هتل"
        verbose_name_plural = "قیمت های هتل"