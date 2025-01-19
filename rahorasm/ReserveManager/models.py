from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django_jalali.db import models as jmodels



class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    tour = models.ForeignKey('TourManager.Tour', on_delete=models.CASCADE, verbose_name="تور")
    hotel_price = models.ForeignKey('HotelManager.HotelPrice', on_delete=models.CASCADE, verbose_name="قیمت هتل")
    two_bed_quantity = models.IntegerField(verbose_name="تعداد دو تخته")
    one_bed_quantity = models.IntegerField(verbose_name="تعداد یک تخته")
    child_with_bed_quantity = models.IntegerField(verbose_name="تعداد کودک با تخت")
    child_no_bed_quantity = models.IntegerField(verbose_name="تعداد کودک بدون تخت")
    final_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name="قیمت نهایی")
    status = models.CharField(max_length=20, choices=[('review', 'در انتظار بررسی'), ('pending', 'در انتظار پرداخت'), ('paid', 'پرداخت شده'), ('canceled', 'لغو شده')], default='review', verbose_name="وضعیت")
    
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return 'رزرو ' + self.user.phone_number

    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزرو ها"
    
    def save(self, *args, **kwargs):

        if self.two_bed_quantity>0:
            self.final_price = self.final_price + self.hotel_price.two_bed_price * self.two_bed_quantity
        if self.one_bed_quantity>0:
            self.final_price = self.final_price + self.hotel_price.one_bed_price * self.one_bed_quantity
        if self.child_with_bed_quantity>0:
            self.final_price = self.final_price + self.hotel_price.child_with_bed_price * self.child_with_bed_quantity
        if self.child_no_bed_quantity>0:
            self.final_price = self.final_price + self.hotel_price.child_no_bed_price * self.child_no_bed_quantity
        super(Reserve, self).save(*args, **kwargs)


class Person(models.Model):
    persian_name = models.CharField(max_length=100, verbose_name="نام فارسی")
    english_name = models.CharField(max_length=100, verbose_name="نام انگلیسی")
    national_code = models.CharField(max_length=10, verbose_name="کد ملی")
    birth_date =  models.CharField(max_length=10, verbose_name="تاریخ تولد")
    passport_number = models.CharField(max_length=10, verbose_name="شماره پاسپورت")
    reserve = models.ForeignKey('Reserve', on_delete=models.CASCADE, verbose_name="رزرو")
    
    class Meta:
        verbose_name = "اطلاعات شخص"
        verbose_name_plural = "اطلاعات اشخاص"