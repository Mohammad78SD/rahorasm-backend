from django.contrib import admin
from .models import ContactDetail, AboutDetail

@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'desc')
    search_fields = ('title',)
    
@admin.register(AboutDetail)
class AboutDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'desc')
    search_fields = ('title',)