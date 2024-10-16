from django.db import models
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from django_ckeditor_5.fields import  CKEditor5Field


class Continent(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    land =CKEditor5Field(verbose_name="سفر با راه و رسم",null=True,blank=True)
    ProsCons = CKEditor5Field(verbose_name="مزایا و  معایب",null=True,blank=True)
    attraction =CKEditor5Field(verbose_name="جاذبه های تورسیتی",null=True,blank=True)
    Bestime = CKEditor5Field(verbose_name="بهترین زمان",null=True,blank=True) 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "قاره"
        verbose_name_plural = "قاره ها"
        
class Country(models.Model):
    name = models.CharField(max_length=200)
    continent = models.ForeignKey(Continent, on_delete=models.PROTECT, related_name='countries')
    land =CKEditor5Field(verbose_name="سفر با راه و رسم",null=True,blank=True)
    ProsCons = CKEditor5Field(verbose_name="مزایا و  معایب",null=True,blank=True)
    attraction =CKEditor5Field(verbose_name="جاذبه های تورسیتی",null=True,blank=True)
    Bestime = CKEditor5Field(verbose_name="بهترین زمان",null=True,blank=True) 
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
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='cities')
    description = models.TextField(null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    land =CKEditor5Field(verbose_name="سفر با راه و رسم",null=True,blank=True)
    ProsCons = CKEditor5Field(verbose_name="مزایا و  معایب",null=True,blank=True)
    attraction =CKEditor5Field(verbose_name="جاذبه های تورسیتی",null=True,blank=True)
    Bestime = CKEditor5Field(verbose_name="بهترین زمان",null=True,blank=True) 
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

class Tour(models.Model):
    title = models.CharField(max_length=200)
    city=models.ForeignKey(City,on_delete=models.PROTECT)
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