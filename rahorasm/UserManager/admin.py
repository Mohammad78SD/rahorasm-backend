from django.contrib import admin

from .models import UserModel, ContactForm

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


admin.site.register(UserModel)
admin.site.register(ContactForm)