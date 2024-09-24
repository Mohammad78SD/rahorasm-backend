from django.db import models
from django.core.exceptions import ValidationError


class ContactDetail(models.Model):
    ICON_CHOICES = [
        ('FaMapLocationDot', 'آیکن نقشه'),
        ('FaEnvelope', 'آیکن ایمیل'),
        ('FaPhoneFlip', 'آیکن تلفن'),
        ('MdAccessTimeFilled', 'آیکن ساعت'),
    ]

    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title
    
class AboutDetail(models.Model):
    ICON_CHOICES = [
        ('MdTravelExplore', 'آیکن سفر'),
        ('FaPlaneDeparture', 'آیکن هواپیما'),
        ('BiTrip', 'آیکن تور'),
        ('FaPassport', 'آیکن پاسپورت'),
        ('BsFillPersonVcardFill', 'آیکن مشتری'),
    ]

    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title