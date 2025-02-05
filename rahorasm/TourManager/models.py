from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models import Min, Max

    
class Continent(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام قاره")
    sort = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_shown = models.BooleanField(default=True, verbose_name="آیا در منو نمایش داده شود؟")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قاره"
        verbose_name_plural = "2. قاره ها"
        
class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام کشور")
    continent = models.ForeignKey(Continent, on_delete=models.PROTECT, related_name='countries', verbose_name="قاره")
    sort = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_shown = models.BooleanField(default=True, verbose_name="آیا در منو نمایش داده شود؟")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "3. کشور ها"
        
class City(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام شهر")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='cities', verbose_name="کشور")
    sort = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_shown = models.BooleanField(default=True, verbose_name="آیا در منو نمایش داده شود؟")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "4. شهر ها"

    
class AirLine(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام هواپیمایی")
    logo = models.ImageField(upload_to='airline_logos/', null=True, blank=True, verbose_name="لوگو")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "هواپیمایی"
        verbose_name_plural = "6. هواپیمایی ها"
    
class Airport(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام فرودگاه")
    short_name = models.CharField(max_length=10, verbose_name="نام کوتاه")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='airports', verbose_name="شهر")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فرودگاه"
        verbose_name_plural = "5. فرودگاه ها"
    

    def save(self, *args, **kwargs):
        self.short_name = self.short_name.upper()
        super().save(*args, **kwargs)
        
        
        
class FlightLeg(models.Model):
    leg_type = models.CharField(max_length=50, choices=[('Departure', 'پرواز رفت'), ('ِContinueDeparture', 'ادامه پرواز رفت'), ('Arrival', 'پرواز برگشت'), ('ContinueArrival', 'ادامه پرواز برگشت')], verbose_name="نوع پرواز", default='Departure')
    flight_length = models.DurationField(verbose_name="مدت پرواز", null=True, blank=True)
    airline = models.ForeignKey(AirLine, on_delete=models.PROTECT, related_name='flight_legs', verbose_name="هواپیمایی")
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='departure_legs', verbose_name="فرودگاه مبدا")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='arrival_legs', verbose_name="فرودگاه مقصد")
    departure_time = jmodels.jDateTimeField(verbose_name="زمان پرواز")
    arrival_time = jmodels.jDateTimeField(verbose_name="زمان فرود")
    stop_time = models.DurationField(verbose_name="زمان توقف", null=True, blank=True)
    travel_class = models.CharField(max_length=50, choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First', 'First')], verbose_name="کلاس سفر")
    class Meta:
        verbose_name = "پرواز"
        verbose_name_plural = "پرواز ها"
    def __str__(self):
        return self.airline.name + ' از ' + self.departure_airport.name + ' به ' + self.arrival_airport.name + ' در تاریخ ' + self.departure_time.strftime('%Y/%m/%d ساعت %H:%M') + ' تا ' + self.arrival_time.strftime('%Y/%m/%d ساعت %H:%M')
    def save(self, *args, **kwargs):
        if self.leg_type == 'Departure' or self.leg_type == 'Arrival':
            self.flight_length = None
        super().save(*args, **kwargs)
        
from HotelManager.models import HotelPrice
class FlightTimes(models.Model):
    departure_date = jmodels.jDateTimeField(verbose_name="تاریخ رفت")
    arrival_date = jmodels.jDateTimeField(verbose_name="تاریخ برگشت")
    flight_Legs = models.ManyToManyField(FlightLeg, related_name='flightLegs', verbose_name="پرواز ها")
    hotel_price = models.ManyToManyField(HotelPrice, related_name='tour_hotels', verbose_name="هتل ها")
    
    
    class Meta:
        verbose_name = "زمان پرواز"
        verbose_name_plural = "زمان های پرواز"
    def __str__(self):
        return 'از '+ self.departure_date.strftime('%Y/%m/%d') + ' تا ' + self.arrival_date.strftime('%Y/%m/%d')
        
class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان تور")
    description_editor = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    occasion = models.CharField(max_length=200, verbose_name="مناسبت", null=True, blank=True)
    image = models.ImageField(upload_to='tour_images/', null=True, blank=True, verbose_name="تصویر")
    start_date = jmodels.jDateField(default=jdatetime.date.today, verbose_name="تاریخ شروع تور")
    destinations = models.ManyToManyField(City, related_name='tours', verbose_name="مقصد تور")
    tour_type = models.CharField(max_length=200, choices=[('هوایی', 'هوایی'), ('زمینی', 'زمینی'), ('دریایی', 'دریایی')], verbose_name="نوع تور")
    needed_documents = models.TextField(verbose_name="مدارک لازم")
    agency_service = models.TextField(verbose_name="خدمات آژانس")
    tour_guide = models.TextField(verbose_name="راهنمای تور")
    tour_duration = models.IntegerField(default=3, verbose_name="مدت زمان تور (شب)")
    is_featured = models.BooleanField(default=False, verbose_name="آیا ویژه است؟")
    is_shown = models.BooleanField(default=True, verbose_name="آیا اعتبار دارد؟")
    least_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="کمترین قیمت تور")
    max_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="بیشترین قیمت تور")
    least_price_currency = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="نرخ ارزی کمترین قیمت تور")
    max_price_currency = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="نرخ ارزی بیشترین قیمت تور")
    other_currency = models.CharField(max_length=200, verbose_name="ارز دیگر", null=True, blank=True)

    flight_times = models.ManyToManyField(FlightTimes, related_name='tour_flights', verbose_name="زمان پرواز", null=True, blank=True)
    
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_prices()  # Update prices after saving

        
    def update_prices(self):
        hotel_prices = HotelPrice.objects.filter(tour_hotels__in=self.flight_times.all())
        # Calculate least price
        if hotel_prices.exists():
            # Get min and max two_bed_price from hotel_prices
            min_price_data = hotel_prices.order_by('two_bed_price').first()
            max_price_data = hotel_prices.order_by('-two_bed_price').first()
            
            min_price = min_price_data.two_bed_price
            least_price_currency = min_price_data.two_bed_price_other_currency
            max_price = max_price_data.two_bed_price
            max_price_currency = max_price_data.two_bed_price_other_currency
            currency = min_price_data.other_currency
            
            # Set the tour's prices
            self.least_price = min_price
            self.least_price_currency = least_price_currency
            self.max_price = max_price
            self.max_price_currency = max_price_currency
            self.other_currency = currency
        else:
            # If no hotel prices found, you can set default values or leave as None
            self.least_price = 0.0
            self.max_price = 0.0
        # Save the updated prices
        super().save(update_fields=['least_price', 'max_price', 'least_price_currency', 'max_price_currency', 'other_currency'])
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "تور"
        verbose_name_plural = "1. تور ها"