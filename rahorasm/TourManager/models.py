from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
    
class Continent(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام قاره")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قاره"
        verbose_name_plural = "قاره ها"
        
class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام کشور")
    continent = models.ForeignKey(Continent, on_delete=models.PROTECT, related_name='countries', verbose_name="قاره")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشور ها"
        
class City(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام شهر")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='cities', verbose_name="کشور")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"

    
class AirLine(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام هواپیمایی")
    logo = models.ImageField(upload_to='airline_logos/', null=True, blank=True, verbose_name="لوگو")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "هواپیمایی"
        verbose_name_plural = "هواپیمایی ها"
    
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
        verbose_name_plural = "فرودگاه ها"
    

    def save(self, *args, **kwargs):
        self.short_name = self.short_name.upper()
        super().save(*args, **kwargs)
    
class Flight(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='flights', verbose_name="تور")
    airline = models.ForeignKey(AirLine, on_delete=models.PROTECT, related_name='flight_airlines', verbose_name="هواپیمایی")
    departure = jmodels.jDateTimeField(verbose_name="زمان پرواز رفت")
    arrival = jmodels.jDateTimeField(verbose_name="زمان فرود رفت")
    origin_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='origin_airport', verbose_name="فرودگاه مبدا")
    destination_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='destination_airport', verbose_name="فرودگاه مقصد")
    return_departure = jmodels.jDateTimeField(verbose_name="زمان پرواز برگشت")
    return_arrival = jmodels.jDateTimeField(verbose_name="زمان فرود برگشت")
    return_origin_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='return_origin_airport', verbose_name="فرودگاه مبدا برگشت")
    return_destination_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='return_destination_airport', verbose_name="فرودگاه مقصد برگشت")
    start_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="شروع قیمت پروازها")
    
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.tour.title} تاریخ {self.departure.strftime("%Y-%m-%d")}'
    class Meta:
        verbose_name = "رفت و برگشت"
        verbose_name_plural = "رفت و برگشت ها"
        
class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان تور")
    description_editor = models.TextField(verbose_name="توضیحات تور", null=True, blank=True)
    occasion = models.CharField(max_length=200, verbose_name="مناسبت", null=True, blank=True)
    image = models.ImageField(upload_to='tour_images/', null=True, blank=True, verbose_name="تصویر")
    start_date = jmodels.jDateField(default=jdatetime.date.today, verbose_name="تاریخ شروع تور")
    destination = models.ForeignKey(City, on_delete=models.PROTECT, related_name='tours', verbose_name="مقصد تور")
    tour_type = models.CharField(max_length=200, choices=[('هوایی', 'هوایی'), ('زمینی', 'زمینی')], verbose_name="نوع تور")
    needed_documents = models.TextField(verbose_name="مدارک لازم")
    agency_service = models.TextField(verbose_name="خدمات آژانس")
    tour_guide = models.TextField(verbose_name="راهنمای تور")
    tour_duration = models.IntegerField(default=3, verbose_name="مدت زمان تور")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_shown = models.BooleanField(default=True, verbose_name="نمایش داده شود")
    least_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="کمترین قیمت تور")
    max_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="بیشترین قیمت تور")

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.update_least_price()
        self.update_max_price()
        
    def update_least_price(self):
        least_price = self.flights.aggregate(models.Min('start_price'))['start_price__min']
        if least_price is not None:
            self.least_price = least_price
            super().save(update_fields=['least_price'])
            
    def update_max_price(self):
        max_price = self.flights.aggregate(models.Max('start_price'))['start_price__max']
        if max_price is not None:
            self.max_price = max_price
            super().save(update_fields=['max_price'])
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "تور"
        verbose_name_plural = "تور ها"