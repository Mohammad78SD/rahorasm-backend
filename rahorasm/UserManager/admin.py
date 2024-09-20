from django.contrib import admin

from .models import UserModel, OTP, ContactForm

admin.site.register(UserModel)
admin.site.register(OTP)
admin.site.register(ContactForm)