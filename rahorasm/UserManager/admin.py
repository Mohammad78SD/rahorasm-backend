from django.contrib import admin

from .models import UserModel, OTP

admin.site.register(UserModel)
admin.site.register(OTP)
