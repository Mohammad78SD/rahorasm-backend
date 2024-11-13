from django.db import models
from django.core.exceptions import ValidationError


class FooterBody(models.Model):
    title = models.CharField(max_length=100, verbose_name="متن لینک")
    link = models.CharField(max_length=100, verbose_name="لینک")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "بخش داخلی فوتر"
        verbose_name_plural = "بخش های داخلی فوتر"
    
class FooterColumn(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان ستون")
    body = models.ManyToManyField(FooterBody, verbose_name="بدنه ستون")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "ستون فوتر"
        verbose_name_plural = "ستون های فوتر"
    
class FooterContact(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر اطلاعات تماس فوتر")
    address = models.TextField(verbose_name="آدرس")
    work_time = models.CharField(max_length=200, verbose_name="ساعت کاری")
    phone = models.TextField(verbose_name="تلفن")
    email = models.EmailField(verbose_name="ایمیل")
    instagram = models.URLField(verbose_name="اینستاگرام")
    telegram = models.URLField(verbose_name="تلگرام")
    whatsapp = models.URLField(verbose_name="واتساپ")
    
    def clean(self):
        if not self.pk and FooterContact.objects.exists():
            raise ValidationError('Only one contact instance is allowed.')

    def save(self, *args, **kwargs):
        if not self.pk and FooterContact.objects.exists():
            return FooterContact.objects.first()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return "اطلاعات تماس"

    class Meta:
        verbose_name = "اطلاعات تماس فوتر"
        verbose_name_plural = "اطلاعات تماس فوتر"
        
class ContactDetail(models.Model):
    ICON_CHOICES = [
        ('material-symbols-light:location-on-rounded', 'آیکن نقشه'),
        ('material-symbols-light:mail-rounded', 'آیکن ایمیل'),
        ('material-symbols-light:phone-enabled', 'آیکن تلفن'),
        ('material-symbols-light:alarm-rounded', 'آیکن ساعت'),
    ]

    icon = models.CharField(max_length=50, choices=ICON_CHOICES, verbose_name="آیکن")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    desc = models.TextField(verbose_name="توضیحات")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "اطلاعات تماس با ما"
        verbose_name_plural = "اطلاعات تماس با ما"
    
class AboutDetail(models.Model):
    ICON_CHOICES = [
        ('material-symbols-light:trip', 'آیکن سفر'),
        ('material-symbols-light:airplane-ticket', 'آیکن هواپیما'),
        ('material-symbols-light:tour', 'آیکن تور'),
        ('material-symbols-light:id-card', 'آیکن پاسپورت'),
        ('material-symbols-light:account-box', 'آیکن مشتری'),
    ]

    icon = models.CharField(max_length=50, choices=ICON_CHOICES, verbose_name="آیکن")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    desc = models.TextField(verbose_name="توضیحات")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "اطلاعات درباره ما"
        verbose_name_plural = "اطلاعات درباره ما"