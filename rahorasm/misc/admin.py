from django.contrib import admin
from .models import ContactDetail, AboutDetail, FooterBody, FooterColumn, FooterContact, MainPagePDF

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
class FooterContactAdmin(admin.ModelAdmin):
  def has_add_permission(self, request):
    num_objects = self.model.objects.count()
    if num_objects >= 1:
      return False
    else:
      return True
admin.site.register(FooterContact, FooterContactAdmin)

class PDFAdmin(admin.ModelAdmin):
  def has_add_permission(self, request):
    num_objects = self.model.objects.count()
    if num_objects >= 1:
      return False
    else:
      return True
admin.site.register(MainPagePDF, PDFAdmin)