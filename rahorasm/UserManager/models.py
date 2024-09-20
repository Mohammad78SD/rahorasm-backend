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


class OTP(models.Model):
    phone_number = models.CharField(unique=True, max_length=15, null=False, blank=False, validators=[phone_regex])
    otp = models.IntegerField()
    otp_expiry = models.DateTimeField()
    max_otp_try = models.IntegerField(default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(null=True, blank=True)



class UserModel(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=15, null=False, blank=False, validators=[phone_regex])
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_email],
    )
    first_login = models.BooleanField(default=False)
    verified = models.BooleanField(default=False, help_text='If otp verification got successful')

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

  
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return self.fname + " " + self.lname

    def get_short_name(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class ContactForm(models.Model):
    SUBJECT_CHOICES = [
        ('TourRegistration', 'ثبت نام تور'),
        ('Suggestions', 'پیشنهادات'),
        ('Complaints', 'انتقادات'),
    ]
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, validators=[phone_regex])
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=200, choices=SUBJECT_CHOICES)
    decription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "فرم تماس"
        verbose_name_plural = "فرم های تماس"