from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, validate_email

phone_regex = RegexValidator(
    regex=r'((0?9)|(\+?989))\d{2}\W?\d{3}\W?\d{4}', message="فرمت شماره تلفن صحیح نیست")
    

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone_number")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.is_active = True
        user.verified = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number=phone_number, password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    
    def create_staffuser(self, phone, password=None):
        user = self.create_user(phone,password=password,is_staff=True,)
        return user




class UserModel(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=15, null=False, blank=False, validators=[phone_regex], verbose_name="شماره تلفن")
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_email],
        verbose_name="ایمیل",
    )
    first_login = models.BooleanField(default=False)
    verified = models.BooleanField(default=False, help_text='If otp verification got successful')

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class ContactForm(models.Model):
    SUBJECT_CHOICES = [
        ('TourRegistration', 'ثبت نام تور'),
        ('Suggestions', 'پیشنهادات'),
        ('Complaints', 'انتقادات'),
    ]
    name = models.CharField(max_length=50, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=15, verbose_name="شماره تلفن")
    email = models.EmailField(max_length=50, verbose_name="ایمیل")
    subject = models.CharField(max_length=200, choices=SUBJECT_CHOICES, verbose_name="موضوع")
    decription = models.TextField(verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "فرم تماس"
        verbose_name_plural = "فرم های تماس"