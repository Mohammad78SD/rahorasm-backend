from django.db import models
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField


class Continent(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قاره"
        verbose_name_plural = "قاره ها"
        
class Country(models.Model):
    name = models.CharField(max_length=200)
    continent = models.ForeignKey(Continent, on_delete=models.PROTECT, related_name='continents')
    description = models.TextField(null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشور ها"
        
class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='counteris')
    description = models.TextField(null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"
    

class AirLine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    logo = ResizedImageField(upload_to="./logo",size=[40,40],null=True)
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
    
class Package(models.Model):
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    rahvarasm = models.CharField(max_length=255,verbose_name="صفر با راه و رسم")
    besttime = models.CharField(max_length=255,verbose_name="بهترین زمان سفر")
    porsCons= models.CharField(max_length=255,verbose_name="مزایا و معایب ")
    atrraction = models.CharField(max_length=255,verbose_name="جاذبه")
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "پکیج"
        verbose_name_plural = "پکیج ها"
    
class Tour(models.Model):
    title = models.CharField(max_length=200)
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='tours')
    description = models.TextField()
    tour_type = models.CharField(max_length=200, choices=[('هوایی', 'هوایی'), ('زمینی', 'زمینی')])
    is_featured = models.BooleanField(default=False)
    tour_duration = models.CharField(max_length=200, default='7 روز')
    needed_documents = models.TextField()
    agency_service = models.TextField()
    tour_guide = models.TextField()
    start_date = jmodels.jDateTimeField()
    end_date = jmodels.jDateTimeField()
    airline = models.ForeignKey(AirLine, on_delete=models.PROTECT)
    origin_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='origin_airport')
    destination_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='destination_airport')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "تور"
        verbose_name_plural = "تور ها"