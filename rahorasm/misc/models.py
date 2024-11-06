from django.db import models
from django.core.exceptions import ValidationError


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