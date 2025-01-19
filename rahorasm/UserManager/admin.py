from django.contrib import admin

from .models import UserModel, ContactForm

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin

class UserModelAdmin(admin.ModelAdmin):
    search_fields = ['phone_number', 'name']
admin.site.register(UserModel, UserModelAdmin)
admin.site.register(ContactForm)