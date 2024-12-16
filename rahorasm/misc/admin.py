from django.contrib import admin
from .models import ContactDetail, AboutDetail, FooterBody, FooterColumn, FooterContact

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'desc')
    search_fields = ('title',)
    
@admin.register(AboutDetail)
class AboutDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'desc')
    search_fields = ('title',)
    
admin.site.register(FooterBody)
admin.site.register(FooterColumn)
admin.site.register(FooterContact)
    