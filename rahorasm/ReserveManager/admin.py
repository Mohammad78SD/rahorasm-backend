from django.contrib import admin
from .models import Reserve, Person

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


admin.site.register(Reserve)
admin.site.register(Person)
