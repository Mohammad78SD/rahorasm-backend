from django.db import models
from django_jalali.db import models as jmodels

class Continent(models.Model):
    name = models.CharField(max_length=200)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قاره"
        verbose_name_plural = "قاره ها"
        
class Country(models.Model):
    name = models.CharField(max_length=200)
    continent = models.ForeignKey(Continent, on_delete=models.PROTECT, related_name='countries')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشور ها"
        
class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='cities')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"
    

class AirLine(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='airline_logos/', null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "هواپیمایی"
        verbose_name_plural = "هواپیمایی ها"
    
class Airport(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
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
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='flights')
    airline = models.ForeignKey(AirLine, on_delete=models.PROTECT, related_name='flight_airlines')
    departure = jmodels.jDateTimeField()
    arrival = jmodels.jDateTimeField()
    origin_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='origin_airport')
    destination_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='destination_airport')
    return_departure = jmodels.jDateTimeField()
    return_arrival = jmodels.jDateTimeField()
    return_origin_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='return_origin_airport')
    return_destination_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='return_destination_airport')
    start_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.tour.title} تاریخ {self.departure}'
    class Meta:
        verbose_name = "رفت و برگشت"
        verbose_name_plural = "رفت و برگشت ها"
        
class Tour(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    destination = models.ForeignKey(City, on_delete=models.PROTECT)
    tour_type = models.CharField(max_length=200, choices=[('هوایی', 'هوایی'), ('زمینی', 'زمینی')])
    needed_documents = models.TextField()
    agency_service = models.TextField()
    tour_guide = models.TextField()
    tour_duration = models.CharField(max_length=200, default='7 روز')
    is_featured = models.BooleanField(default=False)
    least_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.update_least_price()
        
    def update_least_price(self):
        least_price = self.flights.aggregate(models.Min('start_price'))['start_price__min']
        if least_price is not None:
            self.least_price = least_price
            super().save(update_fields=['least_price'])
        
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "تور"
        verbose_name_plural = "تور ها"