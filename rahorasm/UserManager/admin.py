from django.contrib import admin

from .models import UserModel, ContactForm

admin.site.register(UserModel)
admin.site.register(ContactForm)