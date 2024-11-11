from django.db import models
from django.core.exceptions import ValidationError


class FooterBody(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
class FooterColumn(models.Model):
    title = models.CharField(max_length=100)
    body = models.ManyToManyField(FooterBody)
    def __str__(self):
        return self.title
    
class FooterContact(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    work_time = models.CharField(max_length=200)
    phone = models.TextField()
    email = models.EmailField()
    instagram = models.URLField()
    telegram = models.URLField()
    whatsapp = models.URLField()
    
    def clean(self):
        if not self.pk and FooterContact.objects.exists():
            raise ValidationError('Only one contact instance is allowed.')

    def save(self, *args, **kwargs):
        if not self.pk and FooterContact.objects.exists():
            return FooterContact.objects.first()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return "اطلاعات تماس"

class ContactDetail(models.Model):
    ICON_CHOICES = [
        ('material-symbols-light:location-on-rounded', 'آیکن نقشه'),
        ('material-symbols-light:mail-rounded', 'آیکن ایمیل'),
        ('material-symbols-light:phone-enabled', 'آیکن تلفن'),
        ('material-symbols-light:alarm-rounded', 'آیکن ساعت'),
    ]

    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title
    
class AboutDetail(models.Model):
    ICON_CHOICES = [
        ('material-symbols-light:trip', 'آیکن سفر'),
        ('material-symbols-light:airplane-ticket', 'آیکن هواپیما'),
        ('material-symbols-light:tour', 'آیکن تور'),
        ('material-symbols-light:id-card', 'آیکن پاسپورت'),
        ('material-symbols-light:account-box', 'آیکن مشتری'),
    ]

    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title